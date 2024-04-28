import streamlit as st
from utils import read_expenses, styler
import plotly.express as px


# styler()
st.set_page_config(page_title="HOLA", page_icon=":bar_chart:", layout="wide")


df = read_expenses()
# Categories
options = st.multiselect("What are your favorite colors", df["category"].unique(), df["category"].unique())

# df = df.loc[df["category"].isin(["FOOD", "TRANSPORT", "HEALTH"])]
st.dataframe(df)  # Same as st.write(df)


df["week_start"] = df["date"].dt.to_period("W").dt.start_time
df["week_number"] = df["week_start"].dt.strftime("%U").astype(int) + 1
weekly_df = df.groupby(["week_start", "week_number", "category"])["amount"].sum().reset_index().set_index("week_start")
fig = px.bar(weekly_df, x=weekly_df.index, y="amount", color="category", text_auto=True)
st.plotly_chart(fig)

# Bar chart of top consumed products
top_consumed_products = df.groupby("description")["amount"].sum().reset_index().sort_values("amount", ascending=False)
fig_top_consumed_products = px.bar(
    top_consumed_products.head(10),
    x="description",
    y="amount",
    title="Top Consumed Products",
)


st.plotly_chart(fig_top_consumed_products)
