# 共享函数和样式
import streamlit as st
import os
from streamlit_option_menu import option_menu

def apply_custom_style():
    """应用自定义样式到Streamlit应用"""
    # 隐藏Streamlit默认菜单和页面选择器的CSS样式
    menu_style_cfg = """<style>
        /* 隐藏主菜单、页脚和页眉 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 隐藏默认的页面选择器 - 多种选择器组合确保隐藏 */
        div[data-testid="stSidebarNav"] {display: none !important;}
        div.css-1d391kg {display: none !important;}
        div.css-163ttbj {display: none !important;}
        div.css-1aehpvj {display: none !important;}
        button[kind="header"] {display: none !important;}
        
        /* 确保侧边栏其他内容正常显示 */
        section[data-testid="stSidebar"] {
            width: 250px !important;
            min-width: 250px !important;
        }
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
        
        /* 卡片样式 */
        .stCard {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            background-color: white;
            margin-bottom: 20px;
        }
        
        /* 指标卡样式 */
        .metric-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #4B8BF5;
        }
        
        /* 指标值样式 */
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        
        /* 指标标签样式 */
        .metric-label {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
    </style>"""
    
    # 应用样式
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

def add_sidebar_navigation(current_page):
    """添加侧边栏导航菜单，高亮当前页面"""
    # 获取当前页面的索引
    pages = {
        "目标检测": 0,
        "去烟处理": 1,
        "去烟效果对比": 1,  # 使用相同的索引，表示它是去烟处理的子页面
        "去烟性能可视化": 1,  # 新增性能可视化子页面
        "模态配准": 2,
        "数据分析": 3,
        "图像对比": 4,
        "视频对比": 5,
        "效果对比": 6
    }
    
    default_index = pages.get(current_page, 0)
    
    with st.sidebar:
        # 添加logo
        logo = r"B:\images\like\dfb598baf82a0c1917d2c855856683c81759312887.jpg"
        st.image(logo, width=200)
        
        # 添加分隔线
        st.markdown("<hr style='margin-top:0; margin-bottom:20px; border:none; height:1px; background-color:#e0e0e0;'>", unsafe_allow_html=True)
        
        # 侧边栏标题样式
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
        
        # 使用option_menu创建导航菜单，修改样式为浅蓝色
        selected = option_menu(
            menu_title="功能导航",
            options=["目标检测", "去烟处理", "模态配准", "数据分析", "图像对比", "视频对比"],
            icons=["house", "cloud-haze2", "layers", "graph-up", "images", "film"],
            menu_icon="list",
            default_index=default_index if current_page not in ["去烟效果对比", "去烟性能可视化"] else 1,  # 如果是子页面，高亮父页面
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f7ff"},  # 修改为浅蓝色背景
                "icon": {"color": "#4B8BF5", "font-size": "18px"},  # 修改图标颜色为蓝色
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin": "0px", 
                    "--hover-color": "#d6e6ff",  # 修改悬停颜色为更浅的蓝色
                    "color": "#2c3e50"  # 修改文字颜色
                },
                "nav-link-selected": {"background-color": "#a8c7fa", "color": "#1a365d"},  # 修改选中背景为浅蓝色
                "menu-title": {
                    "font-size": "20px", 
                    "font-weight": "bold", 
                    "color": "#4B8BF5", 
                    "text-align": "center", 
                    "margin-bottom": "10px"
                }
            }
        )
        
        # 如果选择了去烟处理，显示子菜单
        if selected == "去烟处理" or current_page in ["去烟处理", "去烟效果对比", "去烟性能可视化"]:
            st.markdown("""
            <style>
            div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
                background-color: #e6f2ff;  /* 更浅的蓝色背景 */
                padding: 5px;
                border-radius: 5px;
                margin-top: 5px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 创建子菜单，修改样式，添加性能可视化选项
            submenu = st.radio(
                "去烟处理功能",
                ["去烟处理", "去烟效果对比", "性能可视化"],
                index=0 if current_page == "去烟处理" else (1 if current_page == "去烟效果对比" else 2),
                horizontal=True,
                key="desmoke_submenu"
            )
            
            # 添加自定义CSS来修改radio按钮的样式
            st.markdown("""
            <style>
            div.row-widget.stRadio > div {
                background-color: #d6e6ff;
                padding: 5px;
                border-radius: 5px;
            }
            div.row-widget.stRadio > div[role="radiogroup"] > label {
                background-color: #f0f7ff;
                border: 1px solid #a8c7fa;
                color: #4B8BF5;
            }
            div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
                background-color: #a8c7fa;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 根据子菜单选择重定向
            if submenu == "去烟处理" and current_page != "去烟处理":
                st.switch_page("pages/1_去烟处理.py")
            elif submenu == "去烟效果对比" and current_page != "去烟效果对比":
                st.switch_page("pages/6_效果对比.py")
            elif submenu == "性能可视化" and current_page != "去烟性能可视化":
                st.switch_page("pages/7_性能可视化.py")
        
        # 处理主菜单页面跳转
        if selected == "目标检测" and current_page not in ["目标检测"]:
            st.switch_page("app.py")
        elif selected == "去烟处理" and current_page not in ["去烟处理", "去烟效果对比", "去烟性能可视化"]:
            st.switch_page("pages/1_去烟处理.py")
        elif selected == "模态配准" and current_page != "模态配准":
            st.switch_page("pages/2_模态配准.py")
        elif selected == "数据分析" and current_page != "数据分析":
            st.switch_page("pages/3_数据分析.py")
        elif selected == "图像对比" and current_page != "图像对比":
            st.switch_page("pages/4_图像对比.py")
        elif selected == "视频对比" and current_page != "视频对比":
            st.switch_page("pages/5_视频对比.py")