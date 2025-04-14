# 模态配准页面
import streamlit as st
import cv2
import numpy as np
import time
import os
import sys
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, add_sidebar_navigation

# 设置页面
st.set_page_config(page_title="智能视频分析系统 - 模态对齐与融合", layout="wide")
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            模态对齐与融合
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        基于特征匹配的多模态视频配准与融合技术
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏导航，替换原来的add_sidebar_header()
add_sidebar_navigation("模态对齐与融合")

# 侧边栏配置
st.sidebar.title("配准参数设置")

# 初始化变量
vid_file_name = ""
processed_video_path = None  # 存储处理后的视频路径
play_demo = False  # 控制是否播放演示视频

# 视频源选择下拉框
source = st.sidebar.selectbox(
    "视频源选择",
    ("上传视频", "演示模式"),  # 两种视频源选项
)

if source == "上传视频":
    # 视频文件上传器
    vid_file = st.sidebar.file_uploader("上传原始视频", type=["mp4", "mov", "avi", "mkv"])
    if vid_file is not None:
        # 保存原始视频
        original_video_path = "original_modal_video.mp4"
        with open(original_video_path, "wb") as f:
            f.write(vid_file.read())
        vid_file_name = original_video_path
        
        # 添加"加载处理后视频"按钮
        if st.sidebar.button("加载并播放"):
            # 获取视频文件名
            video_name = os.path.basename(vid_file.name)
            base_name = os.path.splitext(video_name)[0]
            
            # 尝试在几个可能的位置查找处理后的视频
            possible_paths = [
                f"registered_{base_name}.mp4",  # 以原文件名为基础
                f"A:/study/FuChuang/code/NpTZnOGYaGd-master/video/processed_{base_name}.mp4",  # 指定文件夹
                "demo_registered.mp4"  # 固定名称
            ]
            
            # 查找第一个存在的处理后视频
            for path in possible_paths:
                if os.path.exists(path):
                    processed_video_path = path
                    st.sidebar.success(f"成功加载处理后视频")
                    play_demo = True  # 设置为True，触发播放
                    break
            
            if not processed_video_path:
                st.sidebar.error("未找到对应的处理后视频")
                # 为了演示，可以提供一个默认的处理后视频
                if os.path.exists("demo_registered.mp4"):
                    processed_video_path = "demo_registered.mp4"
                    st.sidebar.info("已加载默认演示视频")
                    play_demo = True  # 设置为True，触发播放
elif source == "演示模式":
    st.sidebar.info("演示模式将使用预设的视频进行展示")
    if st.sidebar.button("开始演示"):
        vid_file_name = "demo_original.mp4"
        processed_video_path = "demo_registered.mp4"
        
        # 检查演示文件是否存在
        if os.path.exists(vid_file_name) and os.path.exists(processed_video_path):
            play_demo = True
            st.sidebar.success("演示视频加载成功")
        else:
            st.sidebar.error("演示视频文件不存在，请确保demo_original.mp4和demo_registered.mp4在当前目录")

# 配准方法选择
registration_method = st.sidebar.selectbox(
    "配准方法",
    ["特征点匹配", "互信息最大化", "光流法", "深度学习方法"]
)

# 配准精度滑块
precision_col1, precision_col2 = st.sidebar.columns([3, 1])
with precision_col1:
    precision = float(st.slider(
        "配准精度", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.8, 
        step=0.05,
        format="%.2f",
        help="配准精度越高，计算时间越长"
    ))
with precision_col2:
    st.markdown(f"""
    <div style="background-color:transparent; padding:8px; border-radius:5px; 
                text-align:center; margin-top:23px; border:1px dashed #d0d0d0;">
        <span style="font-weight:bold; color:#4B8BF5;">{precision:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

# 创建两列布局
col1, col2 = st.columns(2)

# 添加视频区域标题
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
            配准后视频
        </h3>
    </div>
    """, unsafe_allow_html=True)

# 视频帧占位符
org_frame = col1.empty()
processed_frame = col2.empty()

# 美化FPS显示
with st.sidebar:
    st.markdown("""
    <div style="background-color:white; padding:10px; border-radius:10px; 
                box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-top:20px;">
        <h4 style="color:#4B8BF5; text-align:center; margin:0;">性能监控</h4>
    </div>
    """, unsafe_allow_html=True)
    
    fps_display = st.empty()

# 播放逻辑
if play_demo and vid_file_name and processed_video_path:
    # 演示模式：平行播放原始视频和处理后视频
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
        
        stop_button = st.button("停止播放")
        
        while cap_original.isOpened() and cap_processed.isOpened():
            start_time = time.time()
            
            ret1, frame1 = cap_original.read()
            ret2, frame2 = cap_processed.read()
            
            if not ret1 or not ret2:
                break
            
            # 显示原始帧和处理后帧
            org_frame.image(frame1, channels="BGR")
            processed_frame.image(frame2, channels="BGR")
            
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