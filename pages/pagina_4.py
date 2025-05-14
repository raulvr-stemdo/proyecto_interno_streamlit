import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Análisis de Reviews")

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

st.header("Análisis de Reviews")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Gráficas")
    
with tab2:
    #Nos quedamos con los pedidos que han sido entregados
    df_entregados= df[df.order_status=="delivered"]
    #eliminamos datos nulos en order_delivered_customer_date
    df= df.dropna(subset=['order_delivered_customer_date'])
    #convertimos las columnas de fecha estimada y fecha de entrega a formato de fecha
    df.order_delivered_customer_date= pd.to_datetime(df.order_delivered_customer_date)
    df.order_estimated_delivery_date= pd.to_datetime(df.order_estimated_delivery_date)
    #creamos una columna 'retraso' para cuando la fecha de entrega es mayor a la estimada
    df_pedidos_reviuw2=df
    df_pedidos_reviuw2['retrasos']= (df_pedidos_reviuw2.order_delivered_customer_date - df_pedidos_reviuw2.order_estimated_delivery_date)
    df_pedidos_reviuw2['retrasos']= df_pedidos_reviuw2['retrasos'].dt.components.days
    #creamos un nuevo dataframe con los pedidos que no han sido retrasados
    df_sin_retraso= df_pedidos_reviuw2[df_pedidos_reviuw2.retrasos<= 0]
    #numero de reviews y el score medio por estado
    df_reviews_y_score= df_sin_retraso.groupby('customer_state').agg({'review_id':'count', 'review_score':'mean'}).reset_index()
    df_reviews_y_score=df_reviews_y_score.rename(columns={"customer_state":"Estado", "review_id":"Numero_review", "review_score": "Score_medio"})
    st.write(df_reviews_y_score)