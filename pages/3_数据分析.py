# 数据分析页面
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, set_page_config, add_sidebar_header

# 设置页面
set_page_config("智能视频分析系统 - 数据分析")
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            视频分析数据统计
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        可视化展示检测结果与处理效果
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏
add_sidebar_header()

# 侧边栏配置
st.sidebar.title("数据分析参数")

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
    
    # 去烟效果数据
    smoke_removal_data = {
        '视频名称': [f'视频_{i}' for i in range(1, 21)],
        '原始烟雾浓度': np.random.uniform(0.3, 0.9, 20).round(2),
        '处理后烟雾浓度': np.random.uniform(0.0, 0.3, 20).round(2),
        '处理时间(s)': np.random.uniform(1.0, 10.0, 20).round(1),
        '视频长度(s)': np.random.randint(10, 60, 20),
        '处理方法': np.random.choice(['方法A', '方法B', '方法C'], 20)
    }
    
    # 模态配准数据
    registration_data = {
        '视频对': [f'视频对_{i}' for i in range(1, 16)],
        '配准方法': np.random.choice(['特征点匹配', '互信息最大化', '光流法', '深度学习方法'], 15),
        '配准精度': np.random.uniform(0.7, 1.0, 15).round(2),
        '处理时间(s)': np.random.uniform(2.0, 15.0, 15).round(1),
        '视频分辨率': np.random.choice(['1080p', '720p', '4K'], 15),
        '帧率': np.random.choice([24, 30, 60], 15)
    }
    
    return {
        '目标检测': pd.DataFrame(detection_data),
        '去烟处理': pd.DataFrame(smoke_removal_data),
        '模态配准': pd.DataFrame(registration_data)
    }

# 数据源选择
data_source = st.sidebar.selectbox(
    "数据来源",
    ("演示数据", "上传CSV文件")
)

# 分析类型选择
analysis_type = st.sidebar.selectbox(
    "分析类型",
    ("目标检测", "去烟处理", "模态配准")
)

# 可视化类型选择
viz_type = st.sidebar.selectbox(
    "可视化类型",
    ("表格", "柱状图", "折线图", "散点图", "饼图", "热力图")
)

# 根据数据来源获取数据
if data_source == "演示数据":
    demo_data = generate_demo_data()
    df = demo_data[analysis_type]
    st.sidebar.success(f"已加载{analysis_type}演示数据")
else:
    uploaded_file = st.sidebar.file_uploader("上传CSV文件", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV文件加载成功")
    else:
        st.sidebar.warning("请上传CSV文件")
        st.stop()

# 显示数据表格
st.subheader("数据预览")
st.dataframe(df, use_container_width=True)

# 数据统计信息
st.subheader("数据统计")
st.write(df.describe())

# 根据分析类型和可视化类型生成图表
st.subheader("数据可视化")

if viz_type == "表格":
    st.dataframe(df, use_container_width=True)

elif viz_type == "柱状图":
    if analysis_type == "目标检测":
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x='检测目标', ax=ax)
        ax.set_title('各类目标检测数量')
        ax.set_xlabel('目标类型')
        ax.set_ylabel('检测数量')
        st.pyplot(fig)
    
    elif analysis_type == "去烟处理":
        fig, ax = plt.subplots(figsize=(10, 6))
        df['烟雾减少率'] = (df['原始烟雾浓度'] - df['处理后烟雾浓度']) / df['原始烟雾浓度']
        sns.barplot(data=df, x='处理方法', y='烟雾减少率', ax=ax)
        ax.set_title('不同处理方法的烟雾减少率')
        ax.set_xlabel('处理方法')
        ax.set_ylabel('烟雾减少率')
        st.pyplot(fig)
    
    elif analysis_type == "模态配准":
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='配准方法', y='配准精度', ax=ax)
        ax.set_title('不同配准方法的精度比较')
        ax.set_xlabel('配准方法')
        ax.set_ylabel('配准精度')
        st.pyplot(fig)

elif viz_type == "折线图":
    if analysis_type == "目标检测":
        # 按时间戳聚合数据
        time_data = df.groupby(pd.Grouper(key='时间戳', freq='4H')).size().reset_index(name='检测数量')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(time_data['时间戳'], time_data['检测数量'], marker='o')
        ax.set_title('目标检测数量随时间变化')
        ax.set_xlabel('时间')
        ax.set_ylabel('检测数量')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    elif analysis_type == "去烟处理":
        fig, ax = plt.subplots(figsize=(12, 6))
        df = df.sort_values('处理时间(s)')
        ax.plot(df['视频名称'], df['原始烟雾浓度'], marker='o', label='处理前')
        ax.plot(df['视频名称'], df['处理后烟雾浓度'], marker='x', label='处理后')
        ax.set_title('处理前后烟雾浓度对比')
        ax.set_xlabel('视频')
        ax.set_ylabel('烟雾浓度')
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    elif analysis_type == "模态配准":
        fig, ax = plt.subplots(figsize=(12, 6))
        df = df.sort_values('配准精度', ascending=False)
        ax.plot(df['视频对'], df['配准精度'], marker='o')
        ax.set_title('不同视频对的配准精度')
        ax.set_xlabel('视频对')
        ax.set_ylabel('配准精度')
        plt.xticks(rotation=45)
        st.pyplot(fig)

elif viz_type == "散点图":
    if analysis_type == "目标检测":
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='位置_x', y='位置_y', hue='检测目标', size='置信度', sizes=(20, 200), ax=ax)
        ax.set_title('检测目标位置分布')
        ax.set_xlabel('X坐标')
        ax.set_ylabel('Y坐标')
        st.pyplot(fig)
    
    elif analysis_type == "去烟处理":
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='处理时间(s)', y='原始烟雾浓度', hue='处理方法', size='视频长度(s)', sizes=(20, 200), ax=ax)
        ax.set_title('处理时间与烟雾浓度关系')
        ax.set_xlabel('处理时间(s)')
        ax.set_ylabel('原始烟雾浓度')
        st.pyplot(fig)
    
    elif analysis_type == "模态配准":
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='处理时间(s)', y='配准精度', hue='配准方法', style='视频分辨率', ax=ax)
        ax.set_title('处理时间与配准精度关系')
        ax.set_xlabel('处理时间(s)')
        ax.set_ylabel('配准精度')
        st.pyplot(fig)

elif viz_type == "饼图":
    if analysis_type == "目标检测":
        fig, ax = plt.subplots(figsize=(10, 6))
        df['检测目标'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_title('检测目标类型分布')
        st.pyplot(fig)
    
    elif analysis_type == "去烟处理":
        fig, ax = plt.subplots(figsize=(10, 6))
        df['处理方法'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_title('处理方法分布')
        st.pyplot(fig)
    
    elif analysis_type == "模态配准":
        fig, ax = plt.subplots(figsize=(10, 6))
        df['配准方法'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_title('配准方法分布')
        st.pyplot(fig)

elif viz_type == "热力图":
    if analysis_type == "目标检测":
        pivot_table = pd.crosstab(df['检测目标'], df['视频源'])
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', ax=ax)
        ax.set_title('不同视频源的目标检测分布')
        st.pyplot(fig)
    
    elif analysis_type == "去烟处理":
        # 创建处理方法和视频长度的交叉表
        df['视频长度分组'] = pd.cut(df['视频长度(s)'], bins=[0, 20, 40, 60], labels=['短', '中', '长'])
        pivot_table = pd.crosstab(df['处理方法'], df['视频长度分组'], values=df['处理时间(s)'], aggfunc='mean')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', ax=ax)
        ax.set_title('不同处理方法在不同视频长度下的平均处理时间')
        st.pyplot(fig)
    
    elif analysis_type == "模态配准":
        # 创建配准方法和视频分辨率的交叉表
        pivot_table = pd.crosstab(df['配准方法'], df['视频分辨率'], values=df['配准精度'], aggfunc='mean')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', ax=ax)
        ax.set_title('不同配准方法在不同视频分辨率下的平均精度')
        st.pyplot(fig)

# 添加下载按钮
st.subheader("数据导出")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="下载数据为CSV",
    data=csv,
    file_name=f'{analysis_type}_数据.csv',
    mime='text/csv',
)