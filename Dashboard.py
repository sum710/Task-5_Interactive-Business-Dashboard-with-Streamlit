import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")

# Title of the dashboard
st.title("Global Superstore Sales and Profit Dashboard")

# Load and preprocess the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order.Date'], errors='coerce')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    df['Sales'] = df['Sales'].fillna(df['Sales'].median())
    df['Profit'] = df['Profit'].fillna(df['Profit'].median())
    df['Region'] = df['Region'].fillna('Unknown')
    df['Category'] = df['Category'].fillna('Unknown')
    df['Sub.Category'] = df['Sub.Category'].fillna('Unknown')
    df['Customer.Name'] = df['Customer.Name'].fillna('Unknown')
    df['Segment'] = df['Segment'].fillna('Unknown')
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Select Region(s)", options=sorted(df['Region'].unique()), default=list(df['Region'].unique()))
categories = st.sidebar.multiselect("Select Category(s)", options=sorted(df['Category'].unique()), default=list(df['Category'].unique()))
subcategories = st.sidebar.multiselect("Select Sub-Category(s)", options=sorted(df['Sub.Category'].unique()), default=list(df['Sub.Category'].unique()))

# Filter data
filtered_df = df[
    (df['Region'].isin(regions)) &
    (df['Category'].isin(categories)) &
    (df['Sub.Category'].isin(subcategories))
]

# KPIs
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")

# Sales by Segment (Pie Chart)
st.subheader("Sales by Customer Segment")
segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
fig_segment = px.pie(segment_sales, values='Sales', names='Segment', title='Sales Distribution by Segment',
                     color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig_segment, use_container_width=True)

# Profit by Category (Bar Chart)
st.subheader("Profit by Category")
category_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index()
fig_category = px.bar(category_profit, x='Category', y='Profit', title='Profit by Category', 
                      color='Category', color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig_category, use_container_width=True)

# Top 5 Customers by Sales (Bar Chart)
st.subheader("Top 5 Customers by Sales")
top_customers = filtered_df.groupby('Customer.Name')['Sales'].sum().nlargest(5).reset_index()
fig_customers = px.bar(top_customers, x='Customer.Name', y='Sales', title='Top 5 Customers by Sales', 
                       color='Customer.Name', color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_customers, use_container_width=True)

# Data preview
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df[['Order.Date', 'Customer.Name', 'Segment', 'Region', 'Category', 'Sub.Category', 'Sales', 'Profit']].head(10))