import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Inicio", layout="wide")

if "df" in st.session_state:
            df = st.session_state["df"]
if "order_payments" in st.session_state:
    order_payments = st.session_state["order_payments"]
if "orders" in st.session_state:
    orders = st.session_state["orders"]

st.write(df)