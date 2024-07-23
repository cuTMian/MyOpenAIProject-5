import os
import json

import pandas
import pandas as pd

from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from text import PROMPT_TEMPLATE

def dataframe_agent(openai_api_key, openai_base_url, dataframe, query):
    if openai_base_url:
        model = ChatOpenAI(model="gpt-3.5-turbo",
                           openai_api_key=openai_api_key,
                           openai_api_base=openai_base_url,
                           temperature=0)
    else:
        model = ChatOpenAI(model="gpt-3.5-turbo",
                           openai_api_key=openai_api_key,
                           temperature=0)

    agent = create_pandas_dataframe_agent(llm=model,
                                          df=dataframe,
                                          agent_executor_kwargs={"handle_parsing_errors": True},
                                          verbose=True)

    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input": prompt})
    response_dict = json.loads(response["output"])
    return response_dict

if __name__ == '__main__':
    df = pandas.read_csv("personal_data.csv")
    qus = "工资大于80000的人有几个"
    res = dataframe_agent(os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_BASE_URL"), df, qus)
    print(res)
