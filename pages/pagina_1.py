import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Análisis de clientes")

if "df" in st.session_state:
            df = pd.DataFrame(st.session_state["df"])

with st.sidebar:
    st.title("Filtros")
    st.session_state.fecha_inicio = st.date_input(
        "📅 Fecha de inicio", 
        st.session_state.get("fecha_inicio", df["order_purchase_date"].min())
    )
    st.session_state.fecha_fin = st.date_input(
        "📅 Fecha de fin", 
        st.session_state.get("fecha_fin", df["order_purchase_date"].max())
    )
    st.divider()
    n_estados = st.slider("Número de estados", 1, len(df["customer_state"].unique()), value=5)

n_ciudades = 5

df_by_date = df[(df["order_purchase_date"] >= pd.to_datetime(st.session_state.fecha_inicio)) & (df["order_purchase_date"] <= pd.to_datetime(st.session_state.fecha_fin))]
customers_by_state = df_by_date.groupby("customer_state").agg({'customer_id':'count'}).sort_values('customer_id', ascending=False).head(n_estados).reset_index()
customers_by_city = df_by_date.groupby("customer_city").agg({'customer_id':'count'}).sort_values('customer_id', ascending=False).head(n_ciudades).reset_index()
customers_by_state_city = df_by_date.groupby(["customer_state", "customer_city"]).agg({'customer_id':'count'}).sort_values('customer_id', ascending=False).reset_index()

columns = ["customer_id", "customer_state", "customer_city", "order_purchase_date"]
st.header("Análisis de clientes")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    # Gráfica por estados
    st.header("Número de clientes por estado")

    fig1, axs1 = plt.subplots(figsize=(8, 3))
    axs1.bar(
            customers_by_state["customer_state"],
            customers_by_state["customer_id"],
            color="#96f97b"
    )
    axs1.set_xlabel("Estados")
    axs1.set_ylabel("Número de clientes")
    st.pyplot(plt)
    
    # Gráfica por ciudades
    st.header("Número de clientes por ciudad")
    fig2, axs2 = plt.subplots(figsize=(8, 3))
    axs2.bar(
            customers_by_city["customer_city"],
            customers_by_city["customer_id"],
            color="#75bbfd"
    )
    axs2.set_xlabel("Ciudades")
    axs2.set_ylabel("Número de clientes")
    st.pyplot(plt)

with tab2:
    st.header("Tabla top clientes por estado")
    st.write(customers_by_state)
    st.header("Tabla top clientes por ciudad")
    st.write(customers_by_city)