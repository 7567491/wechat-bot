import streamlit as st
import json
import os

# 配置项分组 - 完整版
CONFIG_GROUPS = {
    "系统设置": {
        "channel_type": "渠道类型 - 机器人运行的平台(wx/telegram等)",
        "hot_reload": "热重载 - 是否启用配置热重载",
        "proxy": "代理设置 - 代理服务器地址",
        "expires_in_seconds": "过期时间 - 会话过期时间(秒)",
        "trigger_by_self": "自触发 - 是否响应自己的消息",
    },
    "模型设置": {
        "model": "默认模型 - 使用的AI模型类型",
        "moonshot_model": "Moonshot模型 - Moonshot使用的模型",
        "moonshot_api_key": "Moonshot密钥 - Moonshot的API密钥",
        "moonshot_api_base": "Moonshot接口 - Moonshot的API地址",
        "linkai_api_key": "LinkAI密钥 - LinkAI的API密钥",
        "linkai_app_code": "LinkAI代码 - LinkAI的应用代码",
        "use_linkai": "使用LinkAI - 是否启用LinkAI服务",
    },
    "对话设置": {
        "temperature": "随机性 - 回复的随机程度 (0-2)",
        "max_tokens": "最大字数 - 单次回复的最大字数",
        "conversation_max_tokens": "会话长度 - 整个会话的最大字数",
        "character_desc": "人设描述 - 机器人的性格设定",
        "single_chat_prefix": "私聊前缀 - 触发私聊的关键词",
        "single_chat_reply_prefix": "私聊回复前缀 - 私聊回复的前缀文本",
        "group_chat_prefix": "群聊前缀 - 触发群聊的关键词",
    },
    "功能开关": {
        "speech_recognition": "语音识别 - 是否启用私聊语音识别",
        "group_speech_recognition": "群语音识别 - 是否启用群聊语音识别",
        "voice_reply_voice": "语音回复 - 是否启用语音回复",
        "text_to_image": "图片生成 - 使用的图片生成模型",
        "voice_to_text": "语音转文字 - 使用的语音识别模型",
        "text_to_voice": "文字转语音 - 使用的语音合成模型",
        "image_create_prefix": "绘图前缀 - 触发绘图的关键词",
    },
    "权限设置": {
        "group_name_white_list": "群白名单 - 允许使用的群聊名称列表",
        "subscribe_msg": "订阅消息 - 用户关注时的欢迎语",
    }
}

# 添加数值类型配置项的类型映射
NUMBER_TYPES = {
    "max_tokens": int,
    "conversation_max_tokens": int,
    "expires_in_seconds": int,
    "temperature": float,
}

def ensure_number_type(key, value):
    """确保数值类型的正确性"""
    if key in NUMBER_TYPES:
        try:
            return NUMBER_TYPES[key](value)
        except (TypeError, ValueError):
            return value
    return value

def render_config_input(key, value, description):
    """渲染单个配置项的输入控件"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        label = description.split(' - ')[0] if ' - ' in description else key
        help_text = description.split(' - ')[1] if ' - ' in description else description
        
        if isinstance(value, bool):
            new_value = st.checkbox(
                f"{key} ({label})",
                value=value,
                help=help_text
            )
        elif isinstance(value, (int, float)) or key in NUMBER_TYPES:
            # 根据类型映射决定使用整数还是浮点数
            is_int = isinstance(value, int) or NUMBER_TYPES.get(key) == int
            if is_int:
                new_value = st.number_input(
                    f"{key} ({label})",
                    value=int(float(value)),  # 处理可能的浮点数输入
                    step=1,
                    help=help_text
                )
                new_value = int(new_value)
            else:
                new_value = st.number_input(
                    f"{key} ({label})",
                    value=float(value),
                    step=0.1,
                    help=help_text
                )
        elif isinstance(value, list):
            default_value = ",".join(map(str, value))
            new_value = st.text_input(
                f"{key} ({label})",
                value=default_value,
                help=help_text + " (多个值用逗号分隔)"
            )
            new_value = new_value.split(",") if new_value else []
        else:
            new_value = st.text_input(
                f"{key} ({label})",
                value=str(value),
                help=help_text
            )
    
    with col2:
        st.markdown(f"**当前值:** `{value}`")
    
    return new_value

def render_config_page():
    st.title("配置编辑器")
    
    try:
        config_path = "config.json"
        if not os.path.exists(config_path):
            st.error("未找到config.json文件")
            return
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 确保数值类型的正确性
            for key, value in config.items():
                config[key] = ensure_number_type(key, value)
        
        # 创建标签页
        tabs = st.tabs(list(CONFIG_GROUPS.keys()) + ["原始JSON"])
        
        # 创建表单
        with st.form("config_form"):
            new_config = config.copy()
            
            for tab_idx, (group_name, group_items) in enumerate(CONFIG_GROUPS.items()):
                with tabs[tab_idx]:
                    st.subheader(group_name)
                    for key, description in group_items.items():
                        if key in config:
                            new_value = render_config_input(
                                key, 
                                config[key], 
                                description
                            )
                            # 确保保存时的类型正确性
                            new_config[key] = ensure_number_type(key, new_value)
            
            with tabs[-1]:
                st.json(config)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.form_submit_button("保存配置"):
                    try:
                        # 保存前再次确保类型正确
                        for key, value in new_config.items():
                            new_config[key] = ensure_number_type(key, value)
                            
                        with open(config_path, 'w', encoding='utf-8') as f:
                            json.dump(new_config, f, indent=4, ensure_ascii=False)
                        st.success("配置已保存！")
                    except Exception as e:
                        st.error(f"保存配置时出错: {str(e)}")
                
    except Exception as e:
        st.error(f"读取配置文件时出错: {str(e)}") 