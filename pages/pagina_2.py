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

# Filtrado por fecha
df_by_date = df[(df["order_purchase_date"] >= pd.to_datetime(st.session_state.fecha_inicio)) & (df["order_purchase_date"] <= pd.to_datetime(st.session_state.fecha_fin))]

# Calculo del nº clientes por estado y ciudad
df=df_by_date.groupby(["customer_city", "customer_state"]).agg({'order_id':'count','customer_id':'count'}).reset_index()

# Calculo del porcentaje de pedidos
df['%_pedidos'] = (df['order_id'] * 100) / df["order_id"].sum()

# Calculo del ratio pedidos/clientes
df['Ratio Pedidos/Clientes'] = (df['order_id']) / (df["customer_id"] )

# Top N
top_n = df.sort_values("%_pedidos", ascending=False).head(n_ciudades).reset_index()
top_n = top_n.drop(columns="index")

top_n["customer_state"] = top_n["customer_state"].map(st.session_state["state_map"])
top_n["customer_city"] = top_n["customer_city"].str.capitalize()
top_n = top_n.rename(columns={"customer_city":"Ciudad", "customer_state":"Estado", "order_id":"Pedidos", "customer_id":"Clientes", "%_pedidos":"Pedidos (%)"})

st.header("Análisis de Pedidos")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Porcentaje de pedidos por ciudad")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_n["Ciudad"], top_n['Pedidos (%)'], color="#ad8150")
    ax.set_xlabel("Porcentaje de pedidos")
    ax.set_ylabel("Ciudades")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x}%'))
    st.pyplot(fig)
    
with tab2:
    st.header("Tabla pedidos")
    st.write(top_n.sort_values(by="Pedidos (%)", ascending=False))