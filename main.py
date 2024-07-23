import pandas as pd
import streamlit as st

from utils import dataframe_agent
from tools import create_chart

st.title("CSV数据分析工具")
with st.sidebar:
    openai_api_key = st.text_input('请输入您的OpenAI API密钥', type='password')
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/api-keys)")
    openai_base_url = st.text_input('如果需要，您可以输入您的api base url')

data = st.file_uploader("上传CSV文件：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

query = st.text_area("请输入您的问题（支持散点图、折线图、条形图）：")
start = st.button("生成回答")
if start and data:
    warning_msg = ""
    if not openai_api_key:
        warning_msg = "请输入您的OpenAI API密钥！"
    elif not data:
        warning_msg = "请上传您的CSV文件"

    if warning_msg:
        st.info(warning_msg)
        st.stop()

    with st.spinner(("AI思考中，请稍等...")):
        response = dataframe_agent(openai_api_key, openai_base_url, st.session_state["df"], query)
        if "answer" in response:
            st.write(response["answer"])
        if "table" in response:
            st.table(pd.DataFrame(response["table"]["data"],
                                  columns=response["table"]["columns"]))
        if "bar" in response:
            create_chart(response["bar"], "bar")
        if "line" in response:
            create_chart(response["line"], "line")
        if "scatter" in response:
            create_chart(response["scatter"], "scatter")

