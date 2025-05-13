import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def main():
    path = "proyecto_interno_streamlit/recursos/Olist_Data/"

    customers = pd.read_csv(path + "olist_customers_dataset.csv")
    order_items = pd.read_csv(path + "olist_order_items_dataset.csv")
    order_payments = pd.read_csv(path + "olist_order_payments_dataset.csv")
    order_reviews = pd.read_csv(path + "olist_order_reviews_dataset.csv")
    products = pd.read_csv(path + "olist_products_dataset.csv")
    sellers = pd.read_csv(path + "olist_sellers_dataset.csv")
    product_category_name_translation = pd.read_csv(path + "product_category_name_translation.csv")

    
    
if __name__ == "__main__":
    main()