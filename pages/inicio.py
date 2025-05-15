import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Inicio", layout="wide")

if "df" in st.session_state:
            df = st.session_state["df"]
if "df2" in st.session_state:
            df2 = st.session_state["df2"]

st.markdown("<h1 style='text-align: center;'>OLIST E-COMMERCE</h1>", unsafe_allow_html=True)
st.write(df)
st.write(df2)