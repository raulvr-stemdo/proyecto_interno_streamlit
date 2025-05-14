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

st.header("Análisis de Pedidos Retrasados")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Gráficas")
    
with tab2:
    #Nos quedamos con los pedidos que han sido entregados
    df2= df[df.order_status=="delivered"]
   
    #eliminamos datos nulos en order_delivered_customer_date
    df2= df2.dropna(subset=['order_delivered_customer_date'])
 
    #convertimos las columnas de fecha estimada y fecha de entrega a formato de fecha
    df2.order_delivered_customer_date= pd.to_datetime(df2.order_delivered_customer_date)
    df2.order_estimated_delivery_date= pd.to_datetime(df2.order_estimated_delivery_date)
   
    #creamos una columna 'retraso' para cuando le fecha de entrega es mayor a la estimada
    df3=df2
    df3['retrasos']= (df3.order_delivered_customer_date - df3.order_estimated_delivery_date)
    df3['retrasos']= df3['retrasos'].dt.components.days 
 
    #creamos un nuevo dataframe con los pedidos que han sido retrasados
    df_retraso= df3[df3.retrasos> 0]
   
    #tiempo medio de dias que se pasan de fecha
    df_retraso['retrasos2']= df_retraso.retrasos
 
    #numero de pedidos que llegan tarde por ciudad
    retrasos_ciudad=df_retraso.groupby('customer_city').agg({'retrasos':'count', 'retrasos2':'mean'}).sort_values('retrasos', ascending= False).reset_index()
    retrasos_ciudad=retrasos_ciudad.rename(columns={"customer_city":"ciudad", "retrasos2":"media_dias_retraso","retraso": "n_pedidos_retrasados"})
 
    #% respecto al total de retrasos
    retrasos_ciudad['%_n_retrasos']=(retrasos_ciudad['retrasos'] * 100) / (retrasos_ciudad['retrasos'].sum())
    st.write(retrasos_ciudad)