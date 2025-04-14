# 图像对比页面 - 图像去烟的子模块
import streamlit as st
import cv2
import numpy as np
import os
from streamlit_image_comparison import image_comparison
import sys
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, add_sidebar_navigation

# 设置页面
st.set_page_config(page_title="智能视频分析系统 - 图像对比", layout="wide")
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            图像处理效果对比
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        基于交互式界面的图像处理效果对比
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏导航，替换原来的add_sidebar_header()
add_sidebar_navigation("图像对比")

# 侧边栏配置
st.sidebar.title("图像对比设置")

# 图片目录
image_dir = "a:/study/FuChuang/code/NpTZnOGYaGd-master/images"

# 确保图片目录存在
if not os.path.exists(image_dir):
    os.makedirs(image_dir)
    st.sidebar.warning(f"已创建图片目录: {image_dir}")

# 获取图片列表
def get_image_pairs():
    """获取处理前后的图片对"""
    pairs = {}
    
    # 检查目录是否存在
    if not os.path.exists(image_dir):
        return pairs
    
    # 查找所有原始图片
    raw_images = [f for f in os.listdir(image_dir) if f.startswith("raw_") and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # 查找对应的处理后图片
    for raw_img in raw_images:
        # 假设处理后图片命名为 processed_xxx.jpg
        processed_img = raw_img.replace("raw_", "processed_")
        if os.path.exists(os.path.join(image_dir, processed_img)):
            # 使用不带前缀的名称作为显示名
            display_name = raw_img.replace("raw_", "")
            pairs[display_name] = (raw_img, processed_img)
    
    return pairs

# 获取图片对
image_pairs = get_image_pairs()

# 如果没有找到图片对，显示上传选项
if not image_pairs:
    st.sidebar.info("未找到处理前后的图片对。请上传图片进行对比。")
    
    # 上传原始图片
    raw_image = st.sidebar.file_uploader("上传原始图片", type=["jpg", "jpeg", "png"])
    if raw_image is not None:
        # 保存原始图片
        raw_path = os.path.join(image_dir, f"raw_{raw_image.name}")
        with open(raw_path, "wb") as f:
            f.write(raw_image.read())
        
        # 上传处理后图片
        processed_image = st.sidebar.file_uploader("上传处理后图片", type=["jpg", "jpeg", "png"])
        if processed_image is not None:
            # 保存处理后图片
            processed_path = os.path.join(image_dir, f"processed_{processed_image.name}")
            with open(processed_path, "wb") as f:
                f.write(processed_image.read())
            
            st.sidebar.success("图片上传成功！请刷新页面查看对比效果。")
            
            # 添加到图片对中
            image_pairs[raw_image.name] = (f"raw_{raw_image.name}", f"processed_{processed_image.name}")
else:
    # 如果找到了图片对，显示选择框
    selected_pair = st.sidebar.selectbox(
        "选择图片对比",
        list(image_pairs.keys()),
        format_func=lambda x: x
    )
    
    # 添加上传新图片的选项
    if st.sidebar.checkbox("上传新的图片对"):
        # 上传原始图片
        raw_image = st.sidebar.file_uploader("上传原始图片", type=["jpg", "jpeg", "png"])
        if raw_image is not None:
            # 保存原始图片
            raw_path = os.path.join(image_dir, f"raw_{raw_image.name}")
            with open(raw_path, "wb") as f:
                f.write(raw_image.read())
            
            # 上传处理后图片
            processed_image = st.sidebar.file_uploader("上传处理后图片", type=["jpg", "jpeg", "png"])
            if processed_image is not None:
                # 保存处理后图片
                processed_path = os.path.join(image_dir, f"processed_{processed_image.name}")
                with open(processed_path, "wb") as f:
                    f.write(processed_image.read())
                
                st.sidebar.success("图片上传成功！请刷新页面查看对比效果。")
                
                # 添加到图片对中
                image_pairs[raw_image.name] = (f"raw_{raw_image.name}", f"processed_{processed_image.name}")

# 显示图片对比
if image_pairs:
    # 如果有图片对，显示选中的图片对比
    if 'selected_pair' in locals():
        raw_img, processed_img = image_pairs[selected_pair]
        
        # 构建完整路径
        raw_path = os.path.join(image_dir, raw_img)
        processed_path = os.path.join(image_dir, processed_img)
        
        # 显示图片对比
        st.markdown(f"### {selected_pair} 处理效果对比")
        
        # 使用image_comparison组件
        image_comparison(
            img1=raw_path,
            img2=processed_path,
            label1="处理前",
            label2="处理后",
            width=1200
        )
        
        # # 显示图片信息
        # col1, col2 = st.columns(2)
        
        # # 读取图片获取信息
        # raw_image = cv2.imread(raw_path)
        # processed_image = cv2.imread(processed_path)
        
        # if raw_image is not None and processed_image is not None:
        #     with col1:
        #         st.markdown("#### 原始图片信息")
        #         st.markdown(f"- 尺寸: {raw_image.shape[1]} x {raw_image.shape[0]} 像素")
        #         st.markdown(f"- 通道数: {raw_image.shape[2]}")
                
        #         # 计算信息熵
        #         raw_entropy = 0
        #         for i in range(3):  # 对RGB三个通道分别计算
        #             hist = cv2.calcHist([raw_image], [i], None, [256], [0, 256])
        #             hist = hist / hist.sum()
        #             raw_entropy -= np.sum(hist * np.log2(hist + 1e-7))
        #         raw_entropy /= 3  # 取平均
                
        #         st.markdown(f"- 信息熵: {raw_entropy:.4f}")
                
        #         # 计算平均梯度
        #         gray_raw = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
        #         sobelx = cv2.Sobel(gray_raw, cv2.CV_64F, 1, 0, ksize=3)
        #         sobely = cv2.Sobel(gray_raw, cv2.CV_64F, 0, 1, ksize=3)
        #         raw_gradient = np.mean(np.sqrt(sobelx**2 + sobely**2))
                
        #         st.markdown(f"- 平均梯度: {raw_gradient:.4f}")
                
        #     with col2:
        #         st.markdown("#### 处理后图片信息")
        #         st.markdown(f"- 尺寸: {processed_image.shape[1]} x {processed_image.shape[0]} 像素")
        #         st.markdown(f"- 通道数: {processed_image.shape[2]}")
                
        #         # 计算信息熵
        #         processed_entropy = 0
        #         for i in range(3):  # 对RGB三个通道分别计算
        #             hist = cv2.calcHist([processed_image], [i], None, [256], [0, 256])
        #             hist = hist / hist.sum()
        #             processed_entropy -= np.sum(hist * np.log2(hist + 1e-7))
        #         processed_entropy /= 3  # 取平均
                
        #         st.markdown(f"- 信息熵: {processed_entropy:.4f}")
                
        #         # 计算平均梯度
        #         gray_processed = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        #         sobelx = cv2.Sobel(gray_processed, cv2.CV_64F, 1, 0, ksize=3)
        #         sobely = cv2.Sobel(gray_processed, cv2.CV_64F, 0, 1, ksize=3)
        #         processed_gradient = np.mean(np.sqrt(sobelx**2 + sobely**2))
                
        #         st.markdown(f"- 平均梯度: {processed_gradient:.4f}")
                
        #     # 显示改进指标
        #     st.markdown("#### 改进指标")
            
        #     # 计算信息熵变化
        #     entropy_change = processed_entropy - raw_entropy
        #     entropy_change_percent = (entropy_change / raw_entropy) * 100 if raw_entropy != 0 else 0
            
        #     # 计算平均梯度变化
        #     gradient_change = processed_gradient - raw_gradient
        #     gradient_change_percent = (gradient_change / raw_gradient) * 100 if raw_gradient != 0 else 0
            
        #     # 显示变化
        #     col1, col2 = st.columns(2)
        #     with col1:
        #         st.metric(
        #             "信息熵变化", 
        #             f"{entropy_change:.4f}", 
        #             f"{entropy_change_percent:.2f}%"
        #         )
        #     with col2:
        #         st.metric(
        #             "平均梯度变化", 
        #             f"{gradient_change:.4f}", 
        #             f"{gradient_change_percent:.2f}%"
        #         )
else:
    # 如果没有图片对，显示提示
    st.info("请在侧边栏上传处理前后的图片进行对比。")
    
    # 显示示例图片
    st.markdown("### 示例效果")
    st.markdown("下面是一个图像处理前后对比的示例：")
    st.image("https://www.webbcompare.com/img/hubble/southern_nebula_700.jpg", caption="示例图片")
    st.markdown("上传您的图片后，您将能够通过拖动分界线来比较处理前后的效果。")