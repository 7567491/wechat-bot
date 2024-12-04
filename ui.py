import streamlit as st
from ui.config import render_config_page

# 设置页面配置
st.set_page_config(
    page_title="ChatBot Config",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/yourrepo',
        'Report a bug': "https://github.com/yourusername/yourrepo/issues",
        'About': "# ChatBot Configuration Interface"
    }
)

# 设置暗色主题
dark_theme = """
    <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .sidebar .sidebar-content {
            background-color: #262730;
        }
        .stButton>button {
            border: 2px solid #FFD700;
            background-color: transparent;
            color: #FFD700;
        }
        .stButton>button:hover {
            background-color: #FFD700;
            color: #0E1117;
        }
    </style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.title("ChatBot管理")
    selected = st.radio(
        "导航",
        ["主页", "登录", "日志", "设置"],
        index=0
    )

# 根据选择显示不同页面
if selected == "设置":
    render_config_page()
elif selected == "主页":
    st.title("主页")
    st.write("欢迎使用ChatBot管理界面")
elif selected == "登录":
    st.title("登录")
    st.write("登录功能开发中...")
elif selected == "日志":
    st.title("日志")
    st.write("日志功能开发中...")

# 页脚
st.markdown("---")
st.markdown("ChatBot管理界面 © 2024") 