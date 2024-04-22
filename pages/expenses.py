import streamlit as st
from utils import read_expenses, styler
import plotly.express as px


# styler()
st.set_page_config(page_title="HOLA", page_icon=":bar_chart:", layout="wide")


df = read_expenses()
st.dataframe(df.drop(columns=["operation"]))  # Same as st.write(df)


# Bar chart of top consumed products
top_consumed_products = (
    df.groupby("descripcion")["cantidad"].sum().reset_index().sort_values("cantidad", ascending=False)
)
fig_top_consumed_products = px.bar(
    top_consumed_products.head(10), x="descripcion", y="monto", title="Top Consumed Products"
)

st.plotly_chart(fig_top_consumed_products)
