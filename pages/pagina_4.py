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

# Filtrado por fecha
df_by_date = df[(df["order_purchase_date"] >= pd.to_datetime(st.session_state.fecha_inicio)) & (df["order_purchase_date"] <= pd.to_datetime(st.session_state.fecha_fin))]

# Nos quedamos con los pedidos que han sido entregados
df = df_by_date[df_by_date.order_status=="delivered"]

# Eliminamos datos nulos en order_delivered_customer_date
df = df_by_date.dropna(subset=['order_delivered_customer_date'])

# Creamos una columna 'retraso' para cuando la fecha de entrega es mayor a la estimada
df = df.copy()
df['retrasos'] = (df.order_delivered_customer_date - df.order_estimated_delivery_date).dt.days.astype(int)

# Creamos un nuevo dataframe con los pedidos que no han sido retrasados
df_sin_retraso= df[df.retrasos<= 0]

# Numero de reviews y el score medio por estado
df_reviews_y_score = df_sin_retraso.groupby('customer_state').agg({'review_id':'count', 'review_score':'mean'}).reset_index()
df_reviews_y_score = df_reviews_y_score.rename(columns={"customer_state":"Estado", "review_id":"Nº Reviews", "review_score": "Puntuación Media"})

# Ordenamos por número de reviews y seleccionamos el top 10
df_reviews_y_score = df_reviews_y_score.sort_values(by="Nº Reviews", ascending=False)
top_10 = df_reviews_y_score.head(10)
resto = df_reviews_y_score.iloc[10:].sum()

resto_row = pd.DataFrame([["Resto", resto["Nº Reviews"], resto["Puntuación Media"] / len(df_reviews_y_score.iloc[10:])]], columns=top_10.columns)
df_top_10 = pd.concat([top_10, resto_row], ignore_index=True)

st.header("Análisis de Reviews")
tab1, tab2 = st.tabs(["📈 Gráficas", "📋 Tablas"])

with tab1:
    st.header("Número de Reviews por estado")
    fig, axs = plt.subplots(figsize=(6, 6))
    colors = plt.cm.tab20(range(len(df_top_10)))
    wedges, texts = axs.pie(
        df_top_10["Nº Reviews"],
        labels=df_top_10["Estado"],
        colors=colors
    )

    # Creamos la leyenda usando el mapa de estado
    if "state_map" in st.session_state:
        state_map = st.session_state["state_map"]
        legend_labels = [f"{state_map.get(state, state)} ({state})" for state in df_top_10["Estado"]]
        axs.legend(wedges, legend_labels, title="Estados", loc="center left", bbox_to_anchor=(1, 0.5))

    st.pyplot(plt)

    

with tab2:
    df_reviews_y_score["Estado"] = df_reviews_y_score["Estado"].map(st.session_state["state_map"])
    st.write(df_reviews_y_score)