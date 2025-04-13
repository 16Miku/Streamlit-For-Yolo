# 效果对比页面
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, add_sidebar_navigation

# 设置页面
st.set_page_config(page_title="智能视频分析系统 - 去烟效果对比", layout="wide")
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            去烟处理效果对比分析
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        基于性能指标的视频去烟处理效果分析
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏导航，使用正确的页面名称
add_sidebar_navigation("去烟效果对比")

# 侧边栏配置
st.sidebar.title("数据分析设置")

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
    frames = 50
    example_data = {
        'Frame': list(range(1, frames + 1)),
        'Entropy(bits)': np.random.uniform(5.0, 7.0, frames),
        'Avg_Gradient': np.random.uniform(10.0, 30.0, frames),
        'PSNR': np.random.uniform(25.0, 35.0, frames),
        'SSIM': np.random.uniform(0.7, 0.95, frames),
        'Processing_Time(ms)': np.random.uniform(20.0, 50.0, frames)
    }
    
    example_df = pd.DataFrame(example_data)
    example_path = os.path.join(performance_dir, "example_metrics.csv")
    example_df.to_csv(example_path, index=False)
    
    st.success("已生成示例数据文件，可以继续分析")
    csv_files = ["example_metrics.csv"]

# 选择CSV文件
selected_csv = st.sidebar.selectbox("选择性能数据文件", csv_files)

# 读取CSV文件
csv_path = os.path.join(performance_dir, selected_csv)

try:
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
        
        # 使用Streamlit原生dataframe替代mitosheet
        st.subheader("数据表格")
        
        # 添加编辑功能
        try:
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                num_rows="dynamic",
                hide_index=False
            )
            
            # 添加下载按钮
            csv = edited_df.to_csv(index=False)
            st.download_button(
                "下载编辑后的CSV",
                csv,
                f"edited_{selected_csv}",
                "text/csv",
                key='download-csv'
            )
        except Exception as e:
            st.error(f"显示数据表格时出错: {e}")
            st.write("原始数据预览:")
            st.write(df.head())
        
        # 数据可视化
        st.subheader("性能指标可视化")
        
        # 选择要可视化的指标
        metrics = df.columns.tolist()
        if 'Frame' in metrics:
            metrics.remove('Frame')  # 移除帧索引列
        
        if not metrics:
            st.warning("没有可用于可视化的指标列")
        else:
            selected_metrics = st.multiselect(
                "选择要可视化的指标",
                metrics,
                default=metrics[:2] if len(metrics) >= 2 else metrics
            )
            
            if selected_metrics:
                try:
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
                    
                    # 添加统计分析
                    st.subheader("统计分析")
                    
                    # 计算选定指标的统计信息
                    stats = df[selected_metrics].describe()
                    st.write(stats)
                    
                    # 添加柱状图比较
                    st.subheader("指标平均值比较")
                    
                    avg_values = df[selected_metrics].mean()
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.bar(avg_values.index, avg_values.values)
                    ax.set_ylabel('平均值')
                    ax.set_title('性能指标平均值比较')
                    ax.grid(True, axis='y')
                    
                    # 旋转x轴标签以便更好地显示
                    plt.xticks(rotation=45)
                    
                    st.pyplot(fig)
                    
                    # 添加相关性分析
                    if len(selected_metrics) > 1:
                        st.subheader("指标相关性分析")
                        
                        corr = df[selected_metrics].corr()
                        
                        fig, ax = plt.subplots(figsize=(10, 8))
                        cax = ax.matshow(corr, cmap='coolwarm')
                        fig.colorbar(cax)
                        
                        # 添加相关系数标签
                        for i in range(len(corr.columns)):
                            for j in range(len(corr.columns)):
                                ax.text(i, j, f"{corr.iloc[j, i]:.2f}", 
                                        va='center', ha='center')
                        
                        ax.set_xticks(range(len(corr.columns)))
                        ax.set_yticks(range(len(corr.columns)))
                        ax.set_xticklabels(corr.columns, rotation=45)
                        ax.set_yticklabels(corr.columns)
                        
                        st.pyplot(fig)
                except Exception as e:
                    st.error(f"生成可视化图表时出错: {e}")
                    st.info("请检查数据格式是否正确，或选择其他指标进行可视化")

except Exception as e:
    st.error(f"处理数据时出错: {e}")
    st.info("请检查CSV文件格式是否正确，或尝试重新生成数据文件")