# 视频对比页面
import streamlit as st
import cv2
import os
import sys
import time
from streamlit_image_comparison import image_comparison
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, set_page_config, add_sidebar_header

# 设置页面
set_page_config("智能视频分析系统 - 视频对比")
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            视频处理效果对比
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        通过拖动分界线查看处理前后的视频效果
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏
add_sidebar_header()

# 侧边栏配置
st.sidebar.title("视频对比设置")

# 视频目录
video_dir = "a:/study/FuChuang/code/NpTZnOGYaGd-master/videos"

# 确保视频目录存在
if not os.path.exists(video_dir):
    os.makedirs(video_dir)
    st.sidebar.warning(f"已创建视频目录: {video_dir}")

# 上传原始视频
raw_video = st.sidebar.file_uploader("上传原始视频", type=["mp4", "mov", "avi"])
if raw_video is not None:
    # 保存原始视频
    raw_video_path = os.path.join(video_dir, f"raw_{raw_video.name}")
    with open(raw_video_path, "wb") as f:
        f.write(raw_video.read())
    
    # 上传处理后视频
    processed_video = st.sidebar.file_uploader("上传处理后视频", type=["mp4", "mov", "avi"])
    if processed_video is not None:
        # 保存处理后视频
        processed_video_path = os.path.join(video_dir, f"processed_{processed_video.name}")
        with open(processed_video_path, "wb") as f:
            f.write(processed_video.read())
        
        st.sidebar.success("视频上传成功！请刷新页面查看对比效果。")

        # 播放视频对比
        cap_original = cv2.VideoCapture(raw_video_path)
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
            
            stop_button = st.button("停止播放")
            
            while cap_original.isOpened() and cap_processed.isOpened():
                start_time = time.time()
                
                ret1, frame1 = cap_original.read()
                ret2, frame2 = cap_processed.read()
                
                if not ret1 or not ret2:
                    break
                
                # 使用image_comparison组件进行帧对比
                image_comparison(
                    img1=cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB),
                    img2=cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB),
                    label1="处理前",
                    label2="处理后",
                    width=700
                )
                
                # 控制播放速度，确保同步
                processing_time = time.time() - start_time
                sleep_time = max(0, frame_time - processing_time)
                time.sleep(sleep_time)
                
                if stop_button:
                    break
            
            cap_original.release()
            cap_processed.release()