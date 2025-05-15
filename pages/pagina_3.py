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

# Filtrado por fecha
df_by_date = df[(df["order_purchase_date"] >= pd.to_datetime(st.session_state.fecha_inicio)) & (df["order_purchase_date"] <= pd.to_datetime(st.session_state.fecha_fin))]

# Nos quedamos con los pedidos que han sido entregados
df = df_by_date[df_by_date.order_status=="delivered"]

# Eliminamos datos nulos en order_delivered_customer_date
df = df.dropna(subset=['order_delivered_customer_date'])

# Creamos una columna 'retraso' para cuando le fecha de entrega es mayor a la estimada
df['retrasos'] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"])
df['retrasos'] = df['retrasos'].dt.components.days 

# Creamos un nuevo dataframe con los pedidos que han sido retrasados
df_retraso = df[df.retrasos > 0].copy()

# Tiempo medio de dias que se pasan de fecha
df_retraso.loc[:, 'retrasos2'] = df_retraso["retrasos"]

# Numero de pedidos que llegan tarde por ciudad
retrasos_ciudad=df_retraso.groupby('customer_city').agg({'retrasos':'count', 'retrasos2':'mean'}).sort_values('retrasos', ascending= False).reset_index()


# % respecto al total de retrasos
retrasos_ciudad['Pedidos Retrasados (%)'] = (retrasos_ciudad['retrasos'] * 100) / (retrasos_ciudad['retrasos'].sum())

retrasos_ciudad=retrasos_ciudad.rename(columns={"customer_city":"Ciudad", "retrasos2":"Media de retraso (dias)","retraso": "Nº Pedidos retrasados", "retrasos":"Pedidos Retrasados"})
retrasos_ciudad["Ciudad"] = retrasos_ciudad["Ciudad"].str.capitalize()

st.header("Análisis de Pedidos Retrasados")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Pedidos retrasados por ciudad")
    retrasos_ciudad = retrasos_ciudad.sort_values("Pedidos Retrasados", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Asignamos un color único a cada ciudad
    colors = plt.cm.tab10.colors
    
    for i, row in retrasos_ciudad.iterrows():
        ax.scatter(row["Pedidos Retrasados"], row["Media de retraso (dias)"],
                   color=colors[i % len(colors)], label=row["Ciudad"],
                   s=row["Pedidos Retrasados (%)"] * 20)
        
    ax.set_xlabel("Nº de retrasos")
    ax.set_ylabel("Media de días")
    ax.legend(title="Ciudades", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.tight_layout()
    st.pyplot(plt)
    
with tab2:
    st.write(retrasos_ciudad)