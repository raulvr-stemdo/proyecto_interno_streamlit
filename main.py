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
    pagina_4 = st.Page("pages/pagina_4.py", title="Análisis de Reviews", icon=":material/star_half:")
    pagina_5 = st.Page("pages/pagina_5.py", title="Análisis de Productos", icon=":material/category:")
    
    pg = st.navigation({
        " Navegación": [inicio],
        "📊 Análisis Principales": [pagina_1, pagina_2, pagina_3, pagina_4],
        "📊 Análisis Adicional": [pagina_5]
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
    # Merges
    if "df" not in st.session_state:
        st.session_state.df = st.session_state["orders"].merge(st.session_state["customers"], on="customer_id", how="left")
        st.session_state.df = st.session_state["df"].merge(st.session_state["order_reviews"], on="order_id", how="left")
    
    if "df2" not in st.session_state:
        st.session_state.df2 = st.session_state["order_items"].merge(st.session_state["products"], on="product_id", how="left")
        st.session_state.df2 = st.session_state["df2"].merge(st.session_state["sellers"], on="seller_id", how="left")
        translation_map = dict(zip(
            st.session_state["product_category_name_translation"]["product_category_name"],
            st.session_state["product_category_name_translation"]["product_category_name_english"]
        ))
        st.session_state.df2["product_category_name"] = st.session_state["df2"]["product_category_name"].map(translation_map)
        

    df = st.session_state["df"]

    # Renombramiento de columnas
    df = df.rename(columns={
        "order_purchase_timestamp": "order_purchase_date",
        "order_delivered_carrier_date": "order_delivered_carrier_date",
        "order_delivered_customer_date": "order_delivered_customer_date",
        "order_estimated_delivery_date": "order_estimated_delivery_date"
    })

    # Fechas a datetime
    df["order_purchase_date"] = pd.to_datetime(df["order_purchase_date"])
    df["order_delivered_carrier_date"] = pd.to_datetime(st.session_state["orders"]["order_delivered_carrier_date"])
    df["order_delivered_customer_date"] = pd.to_datetime(st.session_state["orders"]["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(st.session_state["orders"]["order_estimated_delivery_date"])

    # Categorias de productos
    df2 = st.session_state["df2"]
    
    df2["product_category_name"] = df2["product_category_name"].fillna("Others")
    df2["product_category_name"] = df2["product_category_name"].str.replace("-", " ")
    df2["product_category_name"] = df2["product_category_name"].str.replace("_", " ")
    df2["product_category_name"] = df2["product_category_name"].str.capitalize()

    st.session_state.df = df
    st.session_state.df2 = df2

    # Map de los estados
    state_map = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapa", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceara", "DF": "Distrito Federal", "ES": "Espirito Santo", "GO": "Goias",
    "MA": "Maranhao", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Para", "PB": "Paraiba", "PR": "Parana", "PE": "Pernambuco", "PI": "Piaui",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondonia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "Sao Paulo",
    "SE": "Sergipe", "TO": "Tocantins"
    }
    st.session_state.state_map = state_map

if __name__ == "__main__":
    main()