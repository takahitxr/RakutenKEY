import streamlit as st
import datetime
import requests
import json
import pandas as pd
import numpy as np


st.title("楽天キーワード")

if st.button("click"):
    st.write("down")

keyword: str = st.text_input("検索名")
data={
    "keyword": keyword
}
filterbutton = st.button("検索")

# if(filterbutton):
# #    df = 
#     st.line_chart(df)