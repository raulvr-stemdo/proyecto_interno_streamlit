import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Análisis de Productos")

if "df" in st.session_state:
            df = st.session_state["df"]
if "df2" in st.session_state:
            df2 = st.session_state["df2"]
 
df2 = df2.rename(columns={"product_id": "Producto (ID)", "price": "Precio", "product_category_name": "Categoria"})

productos_mas_demanda = df2.groupby(["Producto (ID)", "Categoria", "Precio"]).agg({'order_id':'count'}).rename(columns={"order_id": "Nº de compras"}).sort_values('Nº de compras', ascending=False).reset_index()
productos_menos_demanda = df2.groupby(["Producto (ID)", "Categoria", "Precio"]).agg({'order_id':'count'}).rename(columns={"order_id": "Nº de compras"}).sort_values('Nº de compras', ascending=True).reset_index()

top_15 = df2.groupby(["Producto (ID)", "Categoria", "Precio"]).agg({'order_id': 'count'}).rename(columns={"order_id": "Nº de compras"}).reset_index()
top_15['Ventas'] = top_15['Precio'] * top_15['Nº de compras']
top_15 = top_15.groupby("Categoria").agg({'Ventas': 'sum'}).sort_values('Ventas', ascending=False).head(15).reset_index()

st.header("Análisis de Productos")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Categorías más demandadas")
    fig1, axs1 = plt.subplots(figsize=(8, 4))
    productos_mas_demanda_categoria = productos_mas_demanda.groupby("Categoria").agg({'Nº de compras': 'sum'}).sort_values('Nº de compras', ascending=False).reset_index().head(15)
    axs1.barh(
            productos_mas_demanda_categoria["Categoria"],
            productos_mas_demanda_categoria["Nº de compras"],
            color="#76FF7B"
    )
    axs1.set_ylabel("Categoría")
    axs1.set_xlabel("Número de compras")
    st.pyplot(fig1)

    st.header("Categorías menos demandadas")
    fig2, axs2 = plt.subplots(figsize=(8, 4))
    productos_menos_demanda_categoria = productos_menos_demanda.groupby("Categoria").agg({'Nº de compras': 'sum'}).sort_values('Nº de compras', ascending=True).reset_index().head(15)
    axs2.barh(
            productos_menos_demanda_categoria["Categoria"],
            productos_menos_demanda_categoria["Nº de compras"],
            color="#FC5A50"
    )
    axs2.set_ylabel("Categoría")
    axs2.set_xlabel("Número de compras")
    st.pyplot(fig2)

    st.divider()

    st.header("Categorías con más ingresos")
    fig3, axs3 = plt.subplots(figsize=(8, 4))
    axs3.barh(
            top_15["Categoria"],
            top_15["Ventas"],
            color="#76FF7B"
    )
    axs3.set_ylabel("Categoría")
    axs3.set_xlabel("Ingresos")
    axs3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x/1000)}k'))
    st.pyplot(fig3)
    
with tab2:
    st.header("Productos más demandados")
    st.write(productos_mas_demanda)

    st.header("Productos menos demandados")
    st.write(productos_menos_demanda)

    st.header("Productos con el precio más alto")
    st.write(df2.groupby(["Producto (ID)", "Categoria", "Precio"])
             .agg({'order_id':'count'})
             .rename(columns={"order_id": "Nº de compras"})
             .sort_values('Precio', ascending=False))

    st.header("Top 15 productos que generan más ingresos")
    st.write(top_15.sort_values('Ventas', ascending=False))