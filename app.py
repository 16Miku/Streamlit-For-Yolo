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

    # 隐藏Streamlit默认菜单的CSS样式
    menu_style_cfg = """<style>MainMenu {visibility: hidden;}</style>"""

    # 主标题的HTML样式配置
    main_title_cfg = """<div><h1 style="color:#FF64DA; text-align:center; font-size:40px; 
                             font-family: 'Archivo', sans-serif; margin-top:-50px;margin-bottom:20px;">
                    Ultralytics YOLO Streamlit Application
                    </h1></div>"""

    # 副标题的HTML样式配置
    sub_title_cfg = """<div><h4 style="color:#042AFF; text-align:center; 
                    font-family: 'Archivo', sans-serif; margin-top:-15px; margin-bottom:50px;">
                    Experience real-time object detection on your webcam with the power of Ultralytics YOLO! 🚀</h4>
                    </div>"""

    # 设置Streamlit页面配置
    st.set_page_config(page_title="Ultralytics Streamlit App", layout="wide", initial_sidebar_state="auto")

    # 应用自定义HTML样式
    st.markdown(menu_style_cfg, unsafe_allow_html=True)
    st.markdown(main_title_cfg, unsafe_allow_html=True)
    st.markdown(sub_title_cfg, unsafe_allow_html=True)

    # 在侧边栏添加Ultralytics logo
    with st.sidebar:
        logo = "https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg"
        st.image(logo, width=250)

    # 侧边栏用户配置区域
    st.sidebar.title("User Configuration")

    # 视频源选择下拉框
    source = st.sidebar.selectbox(
        "Video",
        ("webcam", "video"),  # 可选摄像头或上传视频文件
    )

    vid_file_name = ""  # 初始化视频文件名变量
    if source == "video":
        # 视频文件上传器，支持mp4/mov/avi/mkv格式
        vid_file = st.sidebar.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv"])
        if vid_file is not None:
            g = io.BytesIO(vid_file.read())  # 将上传文件读取为字节流
            vid_location = "ultralytics.mp4"  # 临时保存文件名
            with open(vid_location, "wb") as out:  # 将字节流写入临时文件
                out.write(g.read())
            vid_file_name = "ultralytics.mp4"  # 设置视频源为临时文件
    elif source == "webcam":
        vid_file_name = 0  # 0表示使用默认摄像头

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
    # 置信度阈值滑块
    conf = float(st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.01))
    # IoU阈值滑块
    iou = float(st.sidebar.slider("IoU Threshold", 0.0, 1.0, 0.45, 0.01))

    # 创建两列布局
    col1, col2 = st.columns(2)
    org_frame = col1.empty()  # 原始视频帧占位符
    ann_frame = col2.empty()  # 标注后的视频帧占位符

    fps_display = st.sidebar.empty()  # FPS显示占位符

    # 开始按钮
    if st.sidebar.button("Start"):
        # 初始化视频捕获
        videocapture = cv2.VideoCapture(vid_file_name)

        if not videocapture.isOpened():
            st.error("Could not open webcam.")

        # 停止按钮
        stop_button = st.button("Stop")

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
