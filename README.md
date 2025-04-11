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

### 图像对比功能

新增图像对比页面，提供以下功能：

1. **交互式图像对比**：
   - 通过左右拖动分界线直观对比处理前后的图像效果
   - 支持上传自定义图像进行对比分析

2. **多种对比模式**：
   - 原始图像与处理后图像对比
   - 不同处理算法效果对比
   - 不同参数设置效果对比

### 视频对比功能

新增视频对比页面，提供以下功能：

1. **实时视频对比**：
   - 同步播放原始视频和处理后视频
   - 通过拖动分界线直观对比处理前后的视频效果

2. **视频源选择**：
   - 支持上传自定义视频
   - 提供演示模式快速体验

### 效果对比分析

新增效果对比分析页面，提供以下功能：

1. **性能指标可视化**：
   - 读取CSV格式的性能数据
   - 提供折线图、柱状图等多种可视化方式
   - 支持多指标对比分析

2. **数据编辑与导出**：
   - 支持在线编辑数据
   - 提供数据下载功能

3. **统计分析**：
   - 自动计算各项指标的统计信息
   - 提供相关性分析功能

## 系统架构

系统由以下几个主要模块组成：

1. **主页面** - 目标检测功能
2. **去烟处理页面** - 视频烟雾去除功能（含性能监控）
3. **模态配准页面** - 多模态视频配准功能
4. **数据分析页面** - 处理结果可视化与统计
5. **图像对比页面** - 处理前后图像效果对比
6. **视频对比页面** - 处理前后视频效果对比
7. **效果对比页面** - 基于性能指标的效果分析
8. **公共工具** - 共享函数和样式

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
- 生成性能对比CSV文件功能

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

# 生成CSV文件按钮
generate_csv_col1, generate_csv_col2 = st.columns([1, 1])
with generate_csv_col1:
    if st.button("生成性能对比CSV文件"):
        # 创建性能数据
        frames = 100  # 假设有100帧
        data = {
            'Frame': list(range(1, frames + 1)),
            'Entropy(bits)': np.random.uniform(5.0, 7.0, frames),
            'Avg_Gradient': np.random.uniform(10.0, 30.0, frames),
            'PSNR': np.random.uniform(25.0, 35.0, frames),
            'SSIM': np.random.uniform(0.7, 0.95, frames),
            'Processing_Time(ms)': np.random.uniform(20.0, 50.0, frames)
        }
        
        # 保存CSV文件
        os.makedirs("perform monitor", exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv("perform monitor/performance_metrics.csv", index=False)
        
        st.success("已生成CSV文件，可在效果对比页面查看详细分析")
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

### 4. 图像对比页面 (pages/4_图像对比.py)

图像对比页面提供了处理前后图像的直观对比功能，支持以下特性：

- 上传原始图像和处理后图像
- 通过拖动分界线直观对比处理效果
- 支持多种图像格式
- 提供演示模式快速体验

#### 核心功能代码解读

```python
# 图像对比组件
image_comparison(
    img1=original_image,
    img2=processed_image,
    label1="原始图像",
    label2="处理后图像",
    width=700
)
```

### 5. 视频对比页面 (pages/5_视频对比.py)

视频对比页面提供了处理前后视频的实时对比功能，支持以下特性：

- 上传原始视频和处理后视频
- 同步播放两个视频
- 通过拖动分界线直观对比处理效果
- 支持多种视频格式
- 提供演示模式快速体验

#### 核心功能代码解读

```python
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
```

### 6. 效果对比页面 (pages/6_效果对比.py)

效果对比页面提供了基于性能指标的视频处理效果分析功能，支持以下特性：

- 读取CSV格式的性能数据
- 多种可视化方式展示性能指标
- 支持数据编辑和导出
- 提供统计分析和相关性分析

#### 核心功能代码解读

```python
# 数据可视化
st.subheader("性能指标可视化")

# 选择要可视化的指标
metrics = df.columns.tolist()
if 'Frame' in metrics:
    metrics.remove('Frame')  # 移除帧索引列

selected_metrics = st.multiselect(
    "选择要可视化的指标",
    metrics,
    default=metrics[:2] if len(metrics) >= 2 else metrics
)

if selected_metrics:
    # 创建折线图
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for metric in selected_metrics:
        ax.plot(df['Frame'] if 'Frame' in df.columns else df.index, 
                df[metric], 
                label=metric)
    
    ax.set_xlabel('帧')
    ax.set_ylabel('指标值')
    ax.set_title('视频处理性能指标')
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
```

## 项目结构

```
NpTZnOGYaGd-master/
├── app.py                  # 主应用入口
├── pages/                  # 多页面应用
│   ├── 1_去烟处理.py        # 去烟处理页面
│   ├── 2_模态配准.py        # 模态配准页面
│   ├── 3_数据分析.py        # 数据分析页面
│   ├── 4_图像对比.py        # 图像对比页面
│   ├── 5_视频对比.py        # 视频对比页面
│   └── 6_效果对比.py        # 效果对比页面
├── utils/                  # 工具函数
│   └── common.py           # 共享函数和样式
├── video/                  # 视频文件目录
├── perform monitor/        # 性能监控数据目录
│   ├── performance_metrics.csv  # 性能指标数据
│   └── raw_image_metrics.csv    # 原始图像指标数据
├── wuxi.yaml               # YOLO模型配置
└── pyproject.toml          # 项目依赖配置
```

## 使用指南

### 安装依赖

首先，确保您已安装Python 3.8或更高版本，然后安装所需依赖：

```bash
pip install streamlit opencv-python numpy pandas matplotlib ultralytics streamlit-image-comparison
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
   - 点击"生成性能对比CSV文件"按钮生成性能数据

3. **图像对比**：
   - 上传原始图像和处理后图像
   - 通过拖动分界线对比处理效果

4. **视频对比**：
   - 上传原始视频和处理后视频
   - 观看同步播放的视频对比效果

5. **效果对比分析**：
   - 选择CSV格式的性能数据文件
   - 选择要可视化的性能指标
   - 查看各种图表和统计分析结果
```
