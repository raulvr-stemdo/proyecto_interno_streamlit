import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def main():
    carga_datasets("recursos/Olist_Data/")
    transformaciones()
    inicio = st.Page("pages/inicio.py", title="Inicio", icon=":material/house:")
    pagina_1 = st.Page("pages/pagina_1.py", title="Análisis de clientes", icon=":material/group:")
    pagina_2 = st.Page("pages/pagina_2.py", title="Análisis de pedidos", icon=":material/local_shipping:")
    pagina_3 = st.Page("pages/pagina_3.py", title="Análisis de Pedidos Retrasados", icon=":material/schedule:")
    pagina_4 = st.Page("pages/pagina_4.py", title="Análisis de Reviews", icon=":material/schedule:")
    
    pg = st.navigation({
        " Navegación": [inicio],
        "📊 Análisis Principales": [pagina_1, pagina_2, pagina_3, pagina_4]
        })
    pg.run()


def carga_datasets(path): # Carga de datasets
    if "customers" not in st.session_state:
        st.session_state.customers = pd.read_csv(path + "olist_customers_dataset.csv")
    if "order_items" not in st.session_state:
        st.session_state.order_items = pd.read_csv(path + "olist_order_items_dataset.csv")
    if "order_payments" not in st.session_state:
        st.session_state.order_payments = pd.read_csv(path + "olist_order_payments_dataset.csv")
    if "order_reviews" not in st.session_state:
        st.session_state.order_reviews = pd.read_csv(path + "olist_order_reviews_dataset.csv")
    if "orders" not in st.session_state:
        st.session_state.orders = pd.read_csv(path + "olist_orders_dataset.csv")
    if "products" not in st.session_state:
        st.session_state.products = pd.read_csv(path + "olist_products_dataset.csv")
    if "sellers" not in st.session_state:
        st.session_state.sellers = pd.read_csv(path + "olist_sellers_dataset.csv")
    if "product_category_name_translation" not in st.session_state:
        st.session_state.product_category_name_translation = pd.read_csv(path + "product_category_name_translation.csv")

def transformaciones():
    if "df" not in st.session_state:
        st.session_state.df = st.session_state["orders"].merge(st.session_state.customers, on="customer_id", how="left")
        st.session_state.df = st.session_state["df"].merge(st.session_state.order_reviews, on="order_id", how="left")
    
    df = st.session_state["df"]
    df = df.rename(columns={
        "order_purchase_timestamp": "order_purchase_date",
        "order_delivered_carrier_date": "order_delivered_carrier_date",
        "order_delivered_customer_date": "order_delivered_customer_date",
        "order_estimated_delivery_date": "order_estimated_delivery_date"
    })
    df["order_purchase_date"] = pd.to_datetime(df["order_purchase_date"])
    df["order_delivered_carrier_date"] = pd.to_datetime(st.session_state["orders"]["order_delivered_carrier_date"])
    df["order_delivered_customer_date"] = pd.to_datetime(st.session_state["orders"]["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(st.session_state["orders"]["order_estimated_delivery_date"])

    st.session_state.df = df

if __name__ == "__main__":
    main()