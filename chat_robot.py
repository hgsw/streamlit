import streamlit as st
import pandas as pd
import time
import datetime


# from streamlit_chatbox import *


@st.cache_resource
def load_data():
    # return pd.read_csv("/data/stream_env/aq_data.csv")
    df = pd.DataFrame(
        {
            "questions": ["什么是呼叫系统？", "我如何选择坐席？"],
            "answer": [
                "通俗理解就是可以打电话的系统。",
                "1、您可以根据产品手册自行查阅相关的操作流程。2、您可以联系客服人员获取帮助。",
            ],
        }
    )
    return df


def main():
    if "first_visit" not in st.session_state:
        st.session_state.first_visit = True
    else:
        st.session_state.first_visit = False
    # 初始化全局配置
    if st.session_state.first_visit:
        # 在这里可以定义任意多个全局变量，方便程序进行调用
        st.session_state.date_time = datetime.datetime.now() + datetime.timedelta(
            hours=8
        )  # Streamlit Cloud的时区是UTC，加8小时即北京时间
        st.snow()

    df = load_data()
    with st.sidebar:
        # st.markdown("## 八度智能问答系统")
        st.sidebar.header("八度智能问答系统")
        st.caption(":fire: [八度云计算官网](https://bdsaas.com/)", )
        # "[八度云计算官网](https://bdsaas.com/)"
        st.sidebar.date_input("当前日期：", st.session_state.date_time.date())
        # st.sidebar.write(f'The current date time is {d}')

        # st.markdown("#### 我可以帮你解决以下问题：")
        st.sidebar.subheader("我可以帮你解决以下问题：")
        for i, value in enumerate(df["questions"], start=1):
            question = f"{i}. {value}"
            st.markdown(question)
        # st.divider() # 分割线

        # btns = st.container()
        # if st.button("清空会话"):
        #     init_session()
        st.button("清空会话", on_click=init_session)

    st.title("Chat Robot")
    st.caption("🚀 Badu intelligence chat robot")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append(
            {"role": "assistant", "content": "你好，有什么可以帮助你吗？"}
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything"):
        prompt = check_len(prompt)
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response = get_answer(prompt, df)
            for trunk in list(response):
                full_response += trunk
                time.sleep(0.15)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            # st.image(
            #     "/data/stream_env/pictures/rootandHuman.png", use_column_width=True
            # )

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    if len(st.session_state.messages) >= 2:
        deleted = st.session_state.messages[-1]
        st.button("删除消息", on_click=delete_message, args={deleted["content"]})


def check_len(prompt):
    if len(prompt) > 100:
        return "输入文本超出限制，请重新输入~"
    else:
        return prompt


def get_answer(prompt, df):
    for row in df.iterrows():
        if prompt == row[1]["questions"]:
            return row[1]["answer"]

    return "抱歉，未找到答案~"


def delete_message(message):
    for msg in st.session_state.messages:
        if msg["content"] == message:
            st.session_state.messages.remove(msg)
            break


def init_session():
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": "你好，有什么可以帮助你吗？"}
    )
