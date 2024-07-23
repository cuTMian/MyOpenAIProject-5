import streamlit as st
import pandas as pd

def create_chart(input_data, type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if type == "bar":
        st.bar_chart(df_data)
    elif type == "line":
        st.line_chart(df_data)
    elif type == "scatter":
        st.scatter_chart(df_data)

