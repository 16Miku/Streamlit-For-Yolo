# Ultralytics YOLO 🚀, AGPL-3.0 license
# 声明代码使用AGPL-3.0许可证

# 导入必要的库
import io  # 用于处理字节流
import time  # 用于时间计算和FPS测量
import cv2  # OpenCV库，用于视频捕获和图像处理
import torch  # PyTorch深度学习框架
import os  # 操作系统接口，用于环境变量设置

# 设置环境变量，解决OpenMP库冲突问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# 从ultralytics工具包导入必要的功能
from ultralytics.utils.checks import check_requirements  # 检查依赖包是否安装
from ultralytics.utils.downloads import GITHUB_ASSETS_STEMS  # 获取GitHub上的模型资源

# 导入自定义工具函数
from utils.common import apply_custom_style, set_page_config, add_sidebar_header


def inference(model=None):
    """
    使用YOLO模型在Streamlit Web应用中实现实时目标检测的主函数
    Args:
        model (str, optional): 预加载的模型路径. Defaults to None.
    """
    # 检查并确保streamlit已安装，版本>=1.29.0
    check_requirements("streamlit>=1.29.0")
    import streamlit as st  # 导入Streamlit库用于构建Web界面
    
    from ultralytics import YOLO  # 导入YOLO模型类

    # 设置页面配置
    set_page_config("智能视频分析系统 - 目标检测")
    
    # 应用自定义样式
    apply_custom_style()

    # 应用自定义HTML样式
    main_title_cfg = """
    <div>
        <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
            font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                智能视频分析系统
        </h1>
    </div>"""
    
    sub_title_cfg = """
    <div>
        <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
            margin-top:-5px; margin-bottom:30px; font-weight:300;">
            基于YOLO的实时目标检测与分析平台
        </h4>
    </div>"""

    st.markdown(main_title_cfg, unsafe_allow_html=True)
    st.markdown(sub_title_cfg, unsafe_allow_html=True)

    # 添加侧边栏头部
    add_sidebar_header()

    # 侧边栏用户配置区域
    st.sidebar.title("用户配置")

    # 视频源选择下拉框
    source = st.sidebar.selectbox(
        "视频源选择",
        ("webcam", "video", "demo_play"),  # 三种视频源选项
    )

    # 以下是原有代码，保持不变
    vid_file_name = ""
    processed_video_path = None  # 存储处理后的视频路径
    play_demo = False  # 控制是否播放演示视频
    
    if source == "video":
        # 视频文件上传器
        vid_file = st.sidebar.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv"])
        if vid_file is not None:
            g = io.BytesIO(vid_file.read())  # 将上传文件读取为字节流
            vid_location = "ultralytics.mp4"  # 临时保存文件名
            with open(vid_location, "wb") as out:  # 将字节流写入临时文件
                out.write(g.read())
            vid_file_name = "ultralytics.mp4"  # 设置视频源为临时文件
    elif source == "webcam":
        vid_file_name = 0  # 0表示使用默认摄像头
    elif source == "demo_play":
        # 演示模式：上传原始视频，自动加载处理后的视频
        # st.sidebar.markdown("### 演示模式")
        # st.sidebar.markdown("上传原始视频，点击按钮后将自动加载处理后的视频并平行播放")
        
        # 上传原始视频
        vid_file = st.sidebar.file_uploader("上传原始视频", type=["mp4", "mov", "avi", "mkv"])
        if vid_file is not None:
            # 保存原始视频
            original_video_path = "original_video.mp4"
            with open(original_video_path, "wb") as f:
                f.write(vid_file.read())
            vid_file_name = original_video_path
            
            # 添加"加载处理后视频"按钮
            if st.sidebar.button("加载并播放"):
                # 这里应该是预先约定好的处理后视频的路径
                # 实际演示时，您需要确保这个路径下有对应的处理后视频
                video_name = os.path.basename(vid_file.name)
                base_name = os.path.splitext(video_name)[0]
                
                # 尝试在几个可能的位置查找处理后的视频
                possible_paths = [
                    f"processed_{base_name}.mp4",  # 以原文件名为基础
                    f"A:/study/FuChuang/code/NpTZnOGYaGd-master/video/processed_{base_name}.mp4",  # 指定文件夹
                    "demo_processed.mp4"  # 固定名称
                ]
                
                # 查找第一个存在的处理后视频
                for path in possible_paths:
                    if os.path.exists(path):
                        processed_video_path = path
                        st.sidebar.success(f"ok")
                        play_demo = True  # 设置为True，触发播放
                        break
                
                if not processed_video_path:
                    st.sidebar.error("error")
                    # 为了演示，可以提供一个默认的处理后视频
                    if os.path.exists("demo_processed.mp4"):
                        processed_video_path = "demo_processed.mp4"
                        st.sidebar.info("已加载默认演示视频")
                        play_demo = True  # 设置为True，触发播放

    # 模型选择下拉框
    available_models = [x.replace("yolo", "YOLO") for x in GITHUB_ASSETS_STEMS if x.startswith("yolo11")]
    if model:
        # 如果有预加载模型，添加到可选模型列表首位
        available_models.insert(0, model.split(".pt")[0])

    # 显示模型选择下拉框
    selected_model = st.sidebar.selectbox("Model", available_models)
    
    # 加载所选YOLO模型
    with st.spinner("Model is downloading..."):
        model = YOLO(f"{selected_model.lower()}.pt")  # 加载模型
        class_names = list(model.names.values())  # 获取模型支持的类别名称列表
    st.success("Model loaded successfully!")  # 显示加载成功消息

    # 类别多选框，默认选择前3个类别
    selected_classes = st.sidebar.multiselect("Classes", class_names, default=class_names[:3])
    # 将选择的类别名称转换为对应的索引
    selected_ind = [class_names.index(option) for option in selected_classes]

    # 确保selected_ind是列表类型
    if not isinstance(selected_ind, list):
        selected_ind = list(selected_ind)

    # 跟踪功能开关
    enable_trk = st.sidebar.radio("Enable Tracking", ("Yes", "No"))
    
    # 添加阈值设置的标题和说明
    st.sidebar.markdown("""
    <div style="background-color:#f8f9fa; padding:10px; border-radius:8px; margin-top:15px; margin-bottom:10px;">
        <h4 style="color:#FF6B6B; margin:0 0 5px 0; font-size:16px;">检测参数设置</h4>
        <p style="color:#666; font-size:12px; margin:0;">
            调整以下参数可以控制检测的精确度和召回率
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 置信度阈值滑块 - 美化版
    conf_col1, conf_col2 = st.sidebar.columns([3, 1])
    with conf_col1:
        conf = float(st.slider(
            "置信度阈值", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.25, 
            step=0.01,
            format="%.2f",
            help="较高的置信度阈值会减少误检，但可能会漏检一些对象"
        ))
    with conf_col2:
        st.markdown(f"""
        <div style="background-color:#e6f3ff; padding:8px; border-radius:5px; 
                    text-align:center; margin-top:23px;">
            <span style="font-weight:bold; color:#4B8BF5;">{conf:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # IoU阈值滑块 - 美化版
    iou_col1, iou_col2 = st.sidebar.columns([3, 1])
    with iou_col1:
        iou = float(st.slider(
            "IoU阈值", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.45, 
            step=0.01,
            format="%.2f",
            help="控制重叠框的过滤程度，较高的值会减少重复检测"
        ))
    with iou_col2:
        # 使用st.markdown创建自定义HTML/CSS样式的数值显示框
        # f-string用于将Python变量(iou)动态插入到HTML中
        st.markdown(f"""
        <div style="background-color:transparent; padding:8px; border-radius:5px; 
                    text-align:center; margin-top:23px; border:1px dashed #d0d0d0;">
            <!-- 样式设计：
                - background-color:transparent：设置透明背景
                - padding:8px：内边距为8像素，使内容不会贴近边缘
                - border-radius:5px：圆角边框，美化显示效果
                - text-align:center：文本居中对齐
                - margin-top:23px：上边距23像素，与滑块垂直对齐
                - border:1px dashed #d0d0d0：添加虚线边框，在透明背景下提供视觉边界
            -->
            <span style="font-weight:bold; color:#4B8BF5;">{iou:.2f}</span>
            <!-- 
                数值显示：
                - font-weight:bold：文字加粗，增强可读性
                - color:#4B8BF5：使用蓝色(#4B8BF5)显示数值，与应用整体色调一致
                - {iou:.2f}：格式化IoU值，保留两位小数
            -->
        </div>
        """, unsafe_allow_html=True)  # unsafe_allow_html=True允许渲染HTML
    
    # 添加参数说明提示
    st.sidebar.markdown("""
    <div style="background-color:#f0f7ff; padding:8px; border-radius:5px; margin-top:5px;">
        <p style="color:#666; font-size:12px; margin:0;">
            <span style="color:#FF6B6B; font-weight:bold;">提示：</span> 
            置信度越高，检测越精确但可能漏检；IoU越高，重叠框过滤越严格。
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 创建两列布局并美化
    col1, col2 = st.columns(2)
    
    # 添加视频区域标题和边框
    with col1:
        st.markdown("""
        <div style="background-color:white; padding:10px; border-radius:10px; 
                    box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;">
            <h3 style="color:#4B8BF5; text-align:center; margin:0;">
                原始视频
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color:white; padding:10px; border-radius:10px; 
                    box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;">
            <h3 style="color:#4B8BF5; text-align:center; margin:0;">
                处理后视频
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    org_frame = col1.empty()  # 原始视频帧占位符
    ann_frame = col2.empty()  # 标注后的视频帧占位符

    # 美化FPS显示
    with st.sidebar:
        st.markdown("""
        <div style="background-color:white; padding:10px; border-radius:10px; 
                    box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-top:20px;">
            <h4 style="color:#4B8BF5; text-align:center; margin:0;">性能监控</h4>
        </div>
        """, unsafe_allow_html=True)
        
        fps_display = st.empty()

    # 修改播放逻辑，增加对demo_play模式的支持
    if st.sidebar.button("Start") or play_demo:
        if source == "demo_play" and processed_video_path and play_demo:
            # 演示模式：平行播放原始视频和处理后视频
            col1.header("原始视频")
            col2.header("处理后视频")
            
            cap_original = cv2.VideoCapture(vid_file_name)
            cap_processed = cv2.VideoCapture(processed_video_path)
            
            if not cap_original.isOpened() or not cap_processed.isOpened():
                st.error("无法打开视频文件，请检查文件路径")
            else:
                # 获取视频帧率，确保同步播放
                fps_original = cap_original.get(cv2.CAP_PROP_FPS)
                fps_processed = cap_processed.get(cv2.CAP_PROP_FPS)
                
                # 使用较低的帧率确保同步
                sync_fps = min(fps_original, fps_processed)
                frame_time = 1.0 / sync_fps if sync_fps > 0 else 0.033  # 默认30fps
                
                stop_button = st.button("Stop")
                
                while cap_original.isOpened() and cap_processed.isOpened():
                    start_time = time.time()
                    
                    ret1, frame1 = cap_original.read()
                    ret2, frame2 = cap_processed.read()
                    
                    if not ret1 or not ret2:
                        break
                    
                    # 显示原始帧和处理后帧
                    org_frame.image(frame1, channels="BGR")
                    ann_frame.image(frame2, channels="BGR")
                    
                    # 控制播放速度，确保同步
                    processing_time = time.time() - start_time
                    sleep_time = max(0, frame_time - processing_time)
                    time.sleep(sleep_time)
                    
                    # 计算并显示FPS
                    actual_fps = 1.0 / (time.time() - start_time)
                    fps_display.metric("FPS", f"{actual_fps:.2f}")
                    
                    if stop_button:
                        break
                
                cap_original.release()
                cap_processed.release()
        else:
            # 原有的实时处理逻辑
            # 开始按钮
            if st.sidebar.button("Start"):
                # 初始化视频捕获
                videocapture = cv2.VideoCapture(vid_file_name)

                if not videocapture.isOpened():
                    st.error("Could not open webcam.")

                # 停止按钮
                # 美化停止按钮
                stop_button_container = st.container()
                with stop_button_container:
                    stop_col1, stop_col2, stop_col3 = st.columns([1, 1, 1])
                    with stop_col2:
                        stop_button = st.button("停止播放", key="stop_button")
                        
                        # 添加按钮样式
                        st.markdown("""
                        <style>
                            div[data-testid="stButton"] button[kind="secondary"] {
                                background-color: #ff5252;
                                color: white;
                                border: none;
                                padding: 8px 16px;
                                font-weight: bold;
                                width: 100%;
                            }
                            div[data-testid="stButton"] button[kind="secondary"]:hover {
                                background-color: #ff3333;
                            }
                        </style>
                        """, unsafe_allow_html=True)

                # 主循环：逐帧处理视频
                while videocapture.isOpened():
                    success, frame = videocapture.read()  # 读取一帧
                    if not success:
                        st.warning("Failed to read frame from webcam. Please make sure the webcam is connected properly.")
                        break

                    prev_time = time.time()  # 记录处理开始时间

                    # 模型推理
                    if enable_trk == "Yes":
                        # 启用跟踪模式
                        results = model.track(frame, conf=conf, iou=iou, classes=selected_ind, persist=True)
                    else:
                        # 普通检测模式
                        results = model(frame, conf=conf, iou=iou, classes=selected_ind)
                    
                    # 在帧上绘制检测结果
                    annotated_frame = results[0].plot()

                    # 计算FPS
                    curr_time = time.time()
                    fps = 1 / (curr_time - prev_time)

                    # 显示原始帧和标注帧
                    org_frame.image(frame, channels="BGR")
                    ann_frame.image(annotated_frame, channels="BGR")

                    # 如果点击停止按钮
                    if stop_button:
                        videocapture.release()  # 释放视频捕获
                        torch.cuda.empty_cache()  # 清空CUDA缓存
                        st.stop()  # 停止Streamlit应用

                    # 更新FPS显示
                    fps_display.metric("FPS", f"{fps:.2f}")

                # 循环结束后释放资源
                videocapture.release()

            # 清空CUDA缓存
            torch.cuda.empty_cache()
            # 销毁所有OpenCV窗口
            cv2.destroyAllWindows()


# 主程序入口
if __name__ == "__main__":
    inference()  # 调用主函数
