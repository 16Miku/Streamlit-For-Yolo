# 性能可视化页面
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import time
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, add_sidebar_navigation

# 设置页面
st.set_page_config(page_title="智能视频分析系统 - 去烟性能可视化", layout="wide")
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            去烟处理性能可视化
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        实时监控与可视化去烟处理性能指标
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏导航，使用正确的页面名称
add_sidebar_navigation("去烟性能可视化")

# 侧边栏配置
st.sidebar.title("性能监控设置")

# 性能数据目录
performance_dir = "a:/study/FuChuang/code/NpTZnOGYaGd-master/perform monitor"

# 确保目录存在
if not os.path.exists(performance_dir):
    os.makedirs(performance_dir)
    st.sidebar.warning(f"已创建性能数据目录: {performance_dir}")

# 获取可用的CSV文件
csv_files = [f for f in os.listdir(performance_dir) if f.endswith('.csv')]

if not csv_files:
    # 如果没有找到CSV文件，自动生成一个示例文件
    st.warning("未找到性能数据文件。正在生成示例数据...")
    
    # 创建示例数据
    frames = 100
    example_data = {
        'Frame': list(range(1, frames + 1)),
        'Entropy(bits)': np.random.uniform(5.0, 7.0, frames),
        'Avg_Gradient': np.random.uniform(10.0, 30.0, frames),
        'PSNR': np.random.uniform(25.0, 35.0, frames),
        'SSIM': np.random.uniform(0.7, 0.95, frames),
        'Processing_Time(ms)': np.random.uniform(20.0, 50.0, frames)
    }
    
    example_df = pd.DataFrame(example_data)
    example_path = os.path.join(performance_dir, "realtime_metrics.csv")
    example_df.to_csv(example_path, index=False)
    
    st.success("已生成示例数据文件，可以继续分析")
    csv_files = ["realtime_metrics.csv"]

# 选择CSV文件
selected_csv = st.sidebar.selectbox("选择性能数据文件", csv_files)

# 读取CSV文件
csv_path = os.path.join(performance_dir, selected_csv)

@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"读取CSV文件时出错: {e}")
        # 返回一个空的DataFrame作为备用
        return pd.DataFrame()

df = load_data(csv_path)

# 检查DataFrame是否为空
if df.empty:
    st.error("数据为空或无法读取，请检查CSV文件格式")
else:
    # 显示数据概览
    st.subheader("数据概览")
    st.write(f"文件名: {selected_csv}")
    st.write(f"数据条数: {len(df)}")
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        # 显示数据表格
        st.subheader("性能数据表格")
        st.dataframe(df.style.highlight_max(axis=0, color='lightgreen').highlight_min(axis=0, color='#ffcccc'))
    
    with col2:
        # 显示统计信息
        st.subheader("统计信息")
        if 'Frame' in df.columns:
            stats_df = df.drop('Frame', axis=1).describe()
        else:
            stats_df = df.describe()
        st.dataframe(stats_df.style.format("{:.2f}"))
    
    # 实时性能监控模拟
    st.subheader("实时性能监控")
    
    # 创建三列布局用于指标卡
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    # 创建指标卡占位符
    entropy_metric = metric_col1.empty()
    gradient_metric = metric_col2.empty()
    time_metric = metric_col3.empty()
    
    # 创建图表占位符
    chart_placeholder = st.empty()
    
    # 创建进度条
    progress_bar = st.progress(0)
    
    # 模拟实时监控
    if st.button("开始实时监控模拟"):
        # 获取数据列
        entropy_col = 'Entropy(bits)' if 'Entropy(bits)' in df.columns else df.columns[1]
        gradient_col = 'Avg_Gradient' if 'Avg_Gradient' in df.columns else df.columns[2]
        time_col = 'Processing_Time(ms)' if 'Processing_Time(ms)' in df.columns else df.columns[-1]
        
        # 创建实时图表数据
        chart_data = pd.DataFrame({
            "帧": [],
            "信息熵": [],
            "平均梯度": [],
            "处理时间": []
        })
        
        # 模拟实时数据流
        total_frames = min(30, len(df))  # 限制为30帧或数据长度
        
        for i in range(total_frames):
            # 更新进度条
            progress_bar.progress((i + 1) / total_frames)
            
            # 获取当前帧数据
            current_frame = df.iloc[i]
            
            # 更新指标卡
            entropy_metric.metric(
                "信息熵 (bits)", 
                f"{current_frame[entropy_col]:.2f}", 
                f"{current_frame[entropy_col] - df[entropy_col].mean():.2f}"
            )
            
            gradient_metric.metric(
                "平均梯度", 
                f"{current_frame[gradient_col]:.2f}", 
                f"{current_frame[gradient_col] - df[gradient_col].mean():.2f}"
            )
            
            time_metric.metric(
                "处理时间 (ms)", 
                f"{current_frame[time_col]:.2f}", 
                f"{current_frame[time_col] - df[time_col].mean():.2f}"
            )
            
            # 更新图表数据
            new_row = pd.DataFrame({
                "帧": [i+1],
                "信息熵": [current_frame[entropy_col]],
                "平均梯度": [current_frame[gradient_col]],
                "处理时间": [current_frame[time_col]]
            })
            
            chart_data = pd.concat([chart_data, new_row], ignore_index=True)
            
            # 绘制实时图表
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(chart_data["帧"], chart_data["信息熵"], label="信息熵", marker='o', color='#4B8BF5')
            ax.plot(chart_data["帧"], chart_data["平均梯度"] / 10, label="平均梯度/10", marker='s', color='#FF6B6B')
            ax.plot(chart_data["帧"], chart_data["处理时间"] / 10, label="处理时间/10", marker='^', color='#06D6A0')
            
            ax.set_xlabel('帧')
            ax.set_ylabel('指标值')
            ax.set_title('实时性能指标监控')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # 设置y轴范围，使图表更稳定
            ax.set_ylim(0, 10)
            
            # 更新图表
            chart_placeholder.pyplot(fig)
            plt.close(fig)
            
            # 模拟处理延迟
            time.sleep(0.3)
    
    # 性能指标可视化
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
    
    # 选择可视化类型
    viz_type = st.radio(
        "选择可视化类型",
        ["折线图", "柱状图", "散点图", "热力图"],
        horizontal=True
    )
    
    if selected_metrics:
        if viz_type == "折线图":
            # 创建折线图
            fig, ax = plt.subplots(figsize=(10, 6))
            
            for metric in selected_metrics:
                ax.plot(df['Frame'] if 'Frame' in df.columns else df.index, 
                        df[metric], 
                        label=metric,
                        marker='o',
                        markersize=4,
                        alpha=0.7)
            
            ax.set_xlabel('帧')
            ax.set_ylabel('指标值')
            ax.set_title('视频处理性能指标')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
            
        elif viz_type == "柱状图":
            # 创建柱状图
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # 计算每个指标的平均值
            avg_values = df[selected_metrics].mean()
            
            # 绘制柱状图
            bars = ax.bar(avg_values.index, avg_values.values, color=['#4B8BF5', '#FF6B6B', '#06D6A0', '#FFD166'])
            
            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.2f}',
                        ha='center', va='bottom', rotation=0)
            
            ax.set_xlabel('性能指标')
            ax.set_ylabel('平均值')
            ax.set_title('性能指标平均值对比')
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
            
        elif viz_type == "散点图":
            if len(selected_metrics) >= 2:
                # 创建散点图
                fig, ax = plt.subplots(figsize=(10, 6))
                
                x_metric = selected_metrics[0]
                y_metric = selected_metrics[1]
                
                scatter = ax.scatter(df[x_metric], df[y_metric], 
                                    alpha=0.7, 
                                    c=df.index if 'Frame' not in df.columns else df['Frame'],
                                    cmap='viridis',
                                    s=50)
                
                # 添加颜色条
                cbar = plt.colorbar(scatter)
                cbar.set_label('帧索引')
                
                ax.set_xlabel(x_metric)
                ax.set_ylabel(y_metric)
                ax.set_title(f'{x_metric} vs {y_metric}')
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # 添加趋势线
                z = np.polyfit(df[x_metric], df[y_metric], 1)
                p = np.poly1d(z)
                ax.plot(df[x_metric], p(df[x_metric]), "r--", alpha=0.8)
                
                # 添加相关系数
                corr = df[x_metric].corr(df[y_metric])
                ax.annotate(f"相关系数: {corr:.2f}", 
                            xy=(0.05, 0.95), 
                            xycoords='axes fraction',
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                
                st.pyplot(fig)
            else:
                st.warning("散点图需要选择至少两个指标")
                
        elif viz_type == "热力图":
            if len(selected_metrics) >= 2:
                # 创建热力图
                fig, ax = plt.subplots(figsize=(10, 8))
                
                # 计算相关系数矩阵
                corr_matrix = df[selected_metrics].corr()
                
                # 绘制热力图
                im = ax.imshow(corr_matrix, cmap='coolwarm')
                
                # 添加颜色条
                cbar = plt.colorbar(im)
                cbar.set_label('相关系数')
                
                # 设置坐标轴标签
                ax.set_xticks(np.arange(len(selected_metrics)))
                ax.set_yticks(np.arange(len(selected_metrics)))
                ax.set_xticklabels(selected_metrics, rotation=45, ha="right")
                ax.set_yticklabels(selected_metrics)
                
                # 在每个单元格中添加相关系数值
                for i in range(len(selected_metrics)):
                    for j in range(len(selected_metrics)):
                        text = ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                                    ha="center", va="center", color="black" if abs(corr_matrix.iloc[i, j]) < 0.7 else "white")
                
                ax.set_title('性能指标相关性热力图')
                
                st.pyplot(fig)
            else:
                st.warning("热力图需要选择至少两个指标")
    
    # 添加下载按钮
    st.subheader("数据导出")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="下载CSV数据",
        data=csv,
        file_name=f"performance_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )