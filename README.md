# 智能视频分析系统

## 项目概述

本项目是一个基于深度学习的智能视频分析系统，主要功能包括目标检测、去烟处理、多模态视频配准和数据分析。系统采用Streamlit构建Web界面，使用YOLO模型进行目标检测，并提供了友好的用户交互体验。该系统适用于安防监控、工业检测和视频处理等多种场景。

## 新增功能

### 性能监控模块

在去烟处理页面中新增了性能监控模块，主要特性包括：

1. **实时数据展示**：
   - 信息熵 (Entropy)：衡量图像信息丰富程度
   - 平均梯度 (Avg Gradient)：反映图像清晰度和边缘信息
   - 每帧处理时间 (Processing Time)：监控算法处理效率

2. **数据来源**：
   - 从`perform monitor/raw_image_metrics.csv`读取预计算的性能指标
   - 支持实时更新显示当前帧的性能数据

3. **可视化展示**：
   - 在侧边栏以指标卡形式展示
   - 数值实时更新，便于监控处理效果

## 系统架构

系统由以下几个主要模块组成：

1. **主页面** - 目标检测功能
2. **去烟处理页面** - 视频烟雾去除功能（含性能监控）
3. **模态配准页面** - 多模态视频配准功能
4. **数据分析页面** - 处理结果可视化与统计
5. **公共工具** - 共享函数和样式

## 功能模块详解

### 1. 主页面 (app.py)

主页面实现了基于YOLO的实时目标检测功能，支持以下特性：

- 多种视频源选择：摄像头、上传视频、演示模式
- 实时目标检测和跟踪
- 检测结果可视化
- 性能监控（FPS显示）
- 支持多种检测参数调整（置信度阈值、IOU阈值等）

#### 核心功能代码解读

```python
def inference(model=None):
    """
    使用YOLO模型在Streamlit Web应用中实现实时目标检测的主函数
    """
    # 导入必要的库和设置页面
    # ...
    
    # 视频源选择
    source = st.sidebar.selectbox(
        "视频源选择",
        ("webcam", "video", "demo_play"),
    )
    
    # 根据不同视频源处理视频
    if source == "video":
        # 处理上传的视频文件
    elif source == "webcam":
        # 使用摄像头
    elif source == "demo_play":
        # 演示模式：上传原始视频，自动加载处理后的视频
```


### 2. 去烟处理页面 (pages/1_去烟处理.py)

去烟处理页面实现了视频烟雾去除功能，支持以下特性：

- 上传含烟视频
- 自动查找和加载处理后的视频
- 原始视频和去烟后视频的对比显示
- 去烟强度参数调整

#### 核心功能代码解读

```python
# 上传视频
uploaded_file = st.sidebar.file_uploader("上传含烟视频", type=["mp4", "mov", "avi"])
if uploaded_file is not None:
    # 保存原始视频
    original_video_path = "original_smoke_video.mp4"
    with open(original_video_path, "wb") as f:
        f.write(uploaded_file.read())
    vid_file_name = original_video_path
    
    # 添加"加载处理后视频"按钮
    if st.sidebar.button("加载并播放"):
        # 获取视频文件名并查找处理后的视频
        video_name = os.path.basename(uploaded_file.name)
        base_name = os.path.splitext(video_name)[0]
        
        # 查找第一个存在的处理后视频
        for path in possible_paths:
            if os.path.exists(path):
                processed_video_path = path
                st.sidebar.success(f"成功加载处理后视频")
                play_demo = True  # 设置为True，触发播放
                break
```

### 3. 模态配准页面 (pages/2_模态配准.py)

模态配准页面实现了多模态视频配准功能，支持以下特性：

- 上传原始视频
- 自动查找和加载配准后的视频
- 原始视频和配准后视频的对比显示
- 配准方法和精度参数调整
- 演示模式支持

#### 核心功能代码解读

```python
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
            # 获取视频文件名并查找处理后的视频
            video_name = os.path.basename(vid_file.name)
            base_name = os.path.splitext(video_name)[0]
            
            # 尝试在几个可能的位置查找处理后的视频
            possible_paths = [
                f"registered_{base_name}.mp4",
                f"A:/study/FuChuang/code/NpTZnOGYaGd-master/video/processed_{base_name}.mp4",
                "demo_registered.mp4"
            ]
```

### 4. 数据分析页面 (pages/3_数据分析.py)

数据分析页面实现了处理结果的可视化与统计功能，支持以下特性：

- 演示数据自动生成
- 支持CSV文件上传
- 多种可视化图表（柱状图、折线图、散点图、饼图、热力图）
- 数据统计与分析
- 结果导出为CSV

#### 核心功能代码解读

```python
# 生成演示数据函数
def generate_demo_data():
    """生成演示用的数据集"""
    # 目标检测数据
    detection_data = {
        '时间戳': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        '检测目标': np.random.choice(['人', '车', '动物', '烟雾', '火焰'], 100),
        '置信度': np.random.uniform(0.5, 1.0, 100).round(2),
        '处理时间(ms)': np.random.randint(20, 100, 100),
        '位置_x': np.random.randint(0, 1920, 100),
        '位置_y': np.random.randint(0, 1080, 100),
        '视频源': np.random.choice(['摄像头1', '摄像头2', '上传视频'], 100)
    }
    
    # 返回包含各类数据的字典
    return {
        '目标检测': pd.DataFrame(detection_data),
        '去烟处理': pd.DataFrame(smoke_removal_data),
        '模态配准': pd.DataFrame(registration_data)
    }

### 4. 公共工具 (utils/common.py)

公共工具模块提供了共享函数和样式，用于统一各页面的外观和行为：

- 自定义样式应用
- 页面配置设置
- 侧边栏头部添加

#### 核心功能代码解读

```python
def apply_custom_style():
    """应用自定义样式到Streamlit应用"""
    # 隐藏Streamlit默认菜单的CSS样式
    menu_style_cfg = """<style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        #header {visibility: hidden;}
    </style>"""
    
    # 全局CSS样式
    global_css = """
    <style>
        /* 全局字体和背景 */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f7fa;
        }
        
        /* 其他样式... */
    </style>
    """
    
    st.markdown(menu_style_cfg, unsafe_allow_html=True)
    st.markdown(global_css, unsafe_allow_html=True)

def set_page_config(title="智能视频分析系统"):
    """设置页面配置"""
    st.set_page_config(
        page_title=title, 
        layout="wide", 
        initial_sidebar_state="auto",
        page_icon="🎯"
    )

def add_sidebar_header():
    """添加侧边栏头部"""
    with st.sidebar:
        # 添加logo和样式
        logo = r"B:\images\like\dfb598baf82a0c1917d2c855856683c81759312887.jpg"
        if os.path.exists(logo):
            st.image(logo, width=80)
        st.markdown("<h2 style='text-align: center; color: #4B8BF5;'>智能视频分析</h2>", unsafe_allow_html=True)
```

## 技术栈

本项目使用了以下技术和库：

1. **前端框架**：
   - Streamlit - 用于构建Web界面

2. **深度学习框架**：
   - PyTorch - 深度学习框架
   - Ultralytics YOLO - 目标检测模型

3. **图像处理**：
   - OpenCV - 视频捕获和图像处理
   - NumPy - 数值计算

4. **其他工具**：
   - Python 3.8+ - 编程语言
   - YAML - 配置文件

## 项目结构

```
NpTZnOGYaGd-master/
├── app.py                  # 主应用入口
├── pages/                  # 多页面应用
│   ├── 1_去烟处理.py        # 去烟处理页面
│   ├── 2_模态配准.py        # 模态配准页面
│   └── 3_数据分析.py        # 数据分析页面
├── utils/                  # 工具函数
│   └── common.py           # 共享函数和样式
├── video/                  # 视频文件目录
├── wuxi.yaml               # YOLO模型配置
└── pyproject.toml          # 项目依赖配置
```

## 使用指南

### 安装依赖

首先，确保您已安装Python 3.8或更高版本，然后运行以下命令安装所需依赖：

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

### 使用流程

1. **目标检测**：
   - 选择视频源（摄像头、上传视频或演示模式）
   - 调整检测参数
   - 查看实时检测结果

2. **去烟处理**：
   - 上传含烟视频
   - 点击"加载并播放"按钮
   - 调整去烟强度参数
   - 对比原始视频和去烟后视频

3. **模态配准**：
   - 选择视频源（上传视频或演示模式）
   - 上传原始视频
   - 点击"加载并播放"按钮
   - 调整配准方法和精度参数
   - 对比原始视频和配准后视频

## 开发者指南

### 添加新功能

1. 在 `pages/` 目录下创建新的页面文件
2. 导入必要的库和公共工具
3. 设置页面配置和样式
4. 实现功能逻辑

### 修改样式

修改 `utils/common.py` 中的 `apply_custom_style()` 函数来更新全局样式。

## 许可证

本项目使用 AGPL-3.0 许可证。详情请参阅 [Ultralytics 许可证](https://ultralytics.com/license)。