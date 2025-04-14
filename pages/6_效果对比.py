# 效果对比页面 - 改名为性能文件
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append("a:/study/FuChuang/code/NpTZnOGYaGd-master")
from utils.common import apply_custom_style, add_sidebar_navigation

# 设置页面
st.set_page_config(page_title="智能视频分析系统 - 性能文件", layout="wide")  # 修改页面标题
apply_custom_style()

# 页面标题
st.markdown("""
<div>
    <h1 style="color:#4B8BF5; text-align:center; font-size:42px; 
        font-family: 'Arial', sans-serif; margin-top:-30px; margin-bottom:10px; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            性能文件分析  <!-- 修改页面标题 -->
    </h1>
</div>
<div>
    <h4 style="color:#555555; text-align:center; font-family: 'Arial', sans-serif; 
        margin-top:-5px; margin-bottom:30px; font-weight:300;">
        基于性能指标的视频去烟处理效果分析
    </h4>
</div>
""", unsafe_allow_html=True)

# 添加侧边栏导航，使用新的页面名称
add_sidebar_navigation("性能文件")  # 修改为"性能文件"

# 性能数据文件路径 - 使用绝对路径
metrics_file_path = "a:/study/FuChuang/code/NpTZnOGYaGd-master/perform monitor/rgb_smoked_dehazed_image_metrics.csv"

# 尝试加载指定的CSV文件
try:
    @st.cache_data
    def load_metrics_data(file_path):
        """加载指定的CSV文件"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"读取CSV文件时出错: {e}")
            return pd.DataFrame()
    
    # 加载CSV文件
    df = load_metrics_data(metrics_file_path)
    
    # 检查DataFrame是否为空
    if df.empty:
        st.error("数据为空或无法读取，请检查CSV文件格式")
    else:
        # # 显示数据概览
        # st.subheader("数据概览")
        # st.write(f"数据来源: rgb_smoked_dehazed_image_metrics.csv")
        # st.write(f"数据条数: {len(df)}")
        
        # # 显示列名和数据类型
        # st.write("数据结构:")
        # st.write(df.dtypes)
        
        # # 显示基本统计信息
        # st.subheader("基本统计信息")
        # st.write(df.describe())
        
        # 使用Streamlit原生dataframe显示数据
        st.subheader("数据表格")
        
        # 添加编辑功能
        try:
            # 使用data_editor显示数据表格
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                num_rows="dynamic",
                hide_index=False,
                column_config={
                    "Image": st.column_config.TextColumn(
                        "图像文件名",
                        width="medium",
                    ),
                    "Entropy(bits)": st.column_config.NumberColumn(
                        "信息熵(bits)",
                        format="%.4f",
                        width="medium",
                    ),
                    "Avg_Gradient": st.column_config.NumberColumn(
                        "平均梯度",
                        format="%.4f",
                        width="medium",
                    ),
                    "processing time/frame": st.column_config.NumberColumn(
                        "每帧处理时间(s)",
                        format="%.6f",
                        width="medium",
                    ),
                }
            )
            
            # 添加下载按钮
            csv = edited_df.to_csv(index=False)
            st.download_button(
                "下载编辑后的CSV",
                csv,
                f"edited_metrics.csv",
                "text/csv",
                key='download-csv'
            )
            
            # # 添加数据可视化
            # st.subheader("数据可视化")
            
            # # 创建两列布局
            # col1, col2 = st.columns(2)
            
            # with col1:
            #     # 信息熵分布图
            #     st.write("信息熵分布")
            #     fig1, ax1 = plt.subplots(figsize=(10, 6))
            #     ax1.hist(df["Entropy(bits)"], bins=20, alpha=0.7, color='blue')
            #     ax1.set_xlabel("信息熵(bits)")
            #     ax1.set_ylabel("频率")
            #     ax1.grid(True, linestyle='--', alpha=0.7)
            #     st.pyplot(fig1)
            
            # with col2:
            #     # 平均梯度分布图
            #     st.write("平均梯度分布")
            #     fig2, ax2 = plt.subplots(figsize=(10, 6))
            #     ax2.hist(df["Avg_Gradient"], bins=20, alpha=0.7, color='green')
            #     ax2.set_xlabel("平均梯度")
            #     ax2.set_ylabel("频率")
            #     ax2.grid(True, linestyle='--', alpha=0.7)
            #     st.pyplot(fig2)
            
            # # 处理时间分布
            # st.write("处理时间分布")
            # fig3, ax3 = plt.subplots(figsize=(10, 6))
            # ax3.hist(df["processing time/frame"], bins=20, alpha=0.7, color='red')
            # ax3.set_xlabel("处理时间(s)")
            # ax3.set_ylabel("频率")
            # ax3.grid(True, linestyle='--', alpha=0.7)
            # st.pyplot(fig3)
            
            # # 信息熵与平均梯度的散点图
            # st.write("信息熵与平均梯度的关系")
            # fig4, ax4 = plt.subplots(figsize=(10, 6))
            # ax4.scatter(df["Entropy(bits)"], df["Avg_Gradient"], alpha=0.5, color='purple')
            # ax4.set_xlabel("信息熵(bits)")
            # ax4.set_ylabel("平均梯度")
            # ax4.grid(True, linestyle='--', alpha=0.7)
            # st.pyplot(fig4)
            
        except Exception as e:
            st.error(f"显示数据表格时出错: {e}")
            st.write("原始数据预览:")
            st.write(df.head())

except Exception as e:
    st.error(f"处理数据时出错: {e}")
    st.info("请检查CSV文件格式是否正确，或确认文件路径是否存在")