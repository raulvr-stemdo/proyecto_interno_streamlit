import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Análisis de pedidos")

if "df" in st.session_state:
            df = st.session_state["df"]

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
    n_ciudades = st.slider("Número de ciudades", 1, 10, value=5)

df2=df.groupby(["customer_city", "customer_state"]).agg({'order_id':'count','customer_id':'count'}).reset_index()
df2 = df2.rename(columns={"customer_city":"ciudad", "customer_state":"estado", "order_id":"numero_pedidos", "customer_id":"numero_clientes"})
df2['%_pedidos'] = (df2['numero_pedidos'] * 100) / df2["numero_pedidos"].sum()
df2['Ratio Pedidos/Clientes'] = (df2['numero_pedidos']) / (df2["numero_clientes"] )
top_n = df2.sort_values("%_pedidos", ascending=False).head(n_ciudades).reset_index()
st.header("Análisis de Pedidos")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Porcentaje de pedidos por ciudad")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_n["ciudad"], top_n['%_pedidos'], color="#ad8150")
    ax.set_xlabel("Porcentaje de pedidos")
    ax.set_ylabel("Ciudades")
    ax.legend()
    st.pyplot(plt)
    
with tab2:
    st.header("Tabla pedidos")
    st.write(top_n.sort_values(by="%_pedidos", ascending=False))