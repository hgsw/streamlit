import streamlit as st
import time
import datetime
import pytz


@st.cache_resource
def load_model():
    # 加载模型文件，暂未实现
    model = None
    tokenizer = None
    return model, tokenizer


def main():
    if "first_visit" not in st.session_state:
        st.session_state.first_visit = True
    else:
        st.session_state.first_visit = False
    if st.session_state.first_visit:
        # 获取当前的 UTC 时间
        utc_now = datetime.datetime.now(tz=pytz.utc)
        # 将 UTC 时间转换为北京时间
        beijing_tz = pytz.timezone("Asia/Shanghai")
        beijing_now = utc_now.astimezone(beijing_tz)

        # 设置 session state 中的 date_time 为北京时间
        st.session_state.date_time = beijing_now
        st.balloons()  # 弹出气球

    # model, tokenizer = load_model()
    with st.sidebar:
        st.sidebar.header("Streamlit 构建 LLM 模型demo")
        st.caption(
            ":fire: [Github 代码](https://github.com/hgsw/streamlit)",
        )
        # 导航栏显示日期
        st.sidebar.date_input("当前日期：", st.session_state.date_time.date())

        st.sidebar.subheader("我可以帮你解决以下问题：")
        background = (
            "我是一个人工智能助手，可以陪你解决各种问题， 比如文本生成，文本概括等。  \n 当前版本我仅仅是一个复读机。"
        )
        st.markdown(background)
        st.sidebar.subheader("危险操作区域：")
        # 导航栏清空会话删除所有历史记录
        st.button("清空会话", on_click=init_session)

    st.title("LLM Chat Robot")
    st.caption("🚀 Intelligence chat robot")

    # 初始化问候消息
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "你好，有什么可以帮助你吗？"})
    # 显示所有历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # 提问框中背景提示语
    if prompt := st.chat_input("Ask anything"):
        # 检查输入文本长度
        prompt = check_len(prompt)
        st.chat_message("user").markdown(prompt)
        # 保存历史
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        # 打印机效果
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response = get_answer(prompt)
            for trunk in list(response):
                full_response += trunk
                time.sleep(0.1)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
    # 保证初始化问候语无法删除
    if len(st.session_state.messages) >= 2:
        deleted = st.session_state.messages[-1]
        st.button("删除消息", on_click=delete_message, args={deleted["content"]})


def check_len(prompt):
    if len(prompt) > 200:
        return "输入文本超出限制，请重新输入~"
    else:
        return prompt


def get_answer(prompt):
    response = f"你的问题是：{prompt}  \n 抱歉，我还未接入大模型，无法提供你的回答~"
    return response


def delete_message(message):
    for msg in st.session_state.messages:
        if msg["content"] == message:
            st.session_state.messages.remove(msg)
            break


def init_session():
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "你好，有什么可以帮助你吗？"})
