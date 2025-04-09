# 共享函数和样式
import streamlit as st

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
        
        /* 侧边栏样式 */
        .css-1d391kg {
            background-color: #f0f2f6;
        }
        
        /* 按钮样式 */
        .stButton>button {
            background-color: #4B8BF5;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #3a7ad5;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* 滑块样式 */
        .stSlider>div>div>div {
            background-color: #4B8BF5;
        }

        /* 滑块两端数字背景样式 */
        .stSlider .st-eb {
            background-color: #4B8BF5 !important;
            color: white !important;
            border-radius: 4px !important;
            padding: 2px 4px !important;
        }
        
        /* 卡片样式 */
        .stBlock {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            background-color: white;
        }
        
        /* 视频框样式 */
        .stImage {
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        /* 标题样式 */
        h1, h2, h3, h4 {
            color: #333;
        }
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
        # 可以替换为您自己的logo
        logo = r"B:\images\like\dfb598baf82a0c1917d2c855856683c81759312887.jpg"
        st.image(logo, width=200)
        
        # 添加分隔线
        st.markdown("<hr style='margin-top:0; margin-bottom:20px; border:none; height:1px; background-color:#e0e0e0;'>", unsafe_allow_html=True)
        
        # 侧边栏标题样式 - 汪汪队立大功主题
        st.markdown("""
        <div style="text-align:center;">
            <h3 style="color:#FF6B6B; margin-bottom:10px; font-family:'Comic Sans MS', cursive; 
                text-shadow: 1px 1px 2px #FFD166;">
                🐾 汪汪队立大功 🐾
            </h3>
            <p style="color:#118AB2; font-size:14px; font-style:italic; margin-top:0;">
                随时待命，随叫随到！
            </p>
        </div>
        """, unsafe_allow_html=True)