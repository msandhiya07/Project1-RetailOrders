import pandas as pd 
import numpy as np
import pg8000 
import streamlit as st

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = pg8000.connect(
        host="project1.cr8gq824s0tj.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="Retailorders",
        user="postgres",
        password="vkbmsbsbb"
    )
    return conn

# Function to execute a query and return the result as a pandas DataFrame
def run_query(query):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        conn.close()



st.markdown("<h1 style='text-align: center; color: black;'>Guvi Data Science</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'> MINI PROJECT </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'> Retail Orders Dashboard </h2>", unsafe_allow_html=True)



self_queries ={# type: ignore
"view table 1": 
"SELECT * FROM orders1;",
"view table 2": 
"SELECT * FROM orders2;",
"Retail orders table":
"SELECT * FROM orders1 AS o1 JOIN orders2 AS o2 ON o1.order_id = o2.order_id;",
"ordering cities alphabetically": 
"SELECT * FROM orders1  ORDER BY city ASC;",
"order id with products": 
"SELECT o1.order_id, o2.sub_category AS products FROM orders1 o1 INNER JOIN orders2 o2 ON o1.order_id = o2.order_id;",
"total saleprice":
"SELECT order_id, SUM(sale_price) AS sale_price FROM orders2 GROUP BY order_id ORDER BY sale_price DESC LIMIT 10;",
"total listprice":
"SELECT product_id, SUM(list_price) AS list_price FROM orders2 GROUP BY product_id ORDER BY list_price DESC LIMIT 10;",
"sum of saleprice": # type: ignore
"SELECT order_id, SUM(sale_price) AS sale_price FROM orders2 GROUP BY order_id ORDER BY sale_price DESC LIMIT 10;",
"sum": # type: ignore
"SELECT SUM(sale_price) AS total FROM orders2;",
"max, min, avg":# type: ignore 
"SELECT MAX(sale_price) AS highest_revenue, MIN(sale_price) AS minimum_sales, AVG(sale_price) AS average_sales FROM orders2;",
"Calculte ranking saleprice":# type: ignore
"SELECT order_id, quantity, sale_price, ROW_NUMBER() OVER (PARTITION BY sub_category ORDER BY sale_price DESC) AS rank FROM orders2;",
"Calculate discount by 20%":# type: ignore
"SELECT o2.order_id, o1.category, o2.sub_category, o2.sale_price,20 AS discount_percentage, (o2.sale_price * 20 / 100) AS discount_value FROM orders1 o1 JOIN orders2 o2 ON o1.order_id = o2.order_id;"
}
guvi_queries = {
"Find top 10 highest revenue generating products": 
"SELECT o1.order_id, o1.category, SUM(sale_price) AS total_revenue FROM orders2 o2 JOIN orders1 o1 ON o1.order_id = o2.order_id GROUP BY o1.order_id, o1.category ORDER BY total_revenue DESC LIMIT 10;",
"Find the top 5 cities with the highest profit margins": 
"SELECT o1.city, o1.country, SUM(o2.profit) AS highest_profit FROM orders2 o2 JOIN orders1 o1 ON o1.order_id = o2.order_id GROUP BY o1.city, o1.country ORDER BY highest_profit DESC LIMIT 5;",
"Calculate the total discount given for each category": 
"SELECT o1.category, SUM(o2.discount) AS total_discount FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY o1.category ORDER BY total_discount DESC;",
"Find the average sale price per product category": 
"SELECT o1.category, AVG(o2.sale_price) AS average_sale_price FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY o1.category ORDER BY average_sale_price DESC;",
"Total profit per category": 
"SELECT o2.sub_category, AVG(o2.sale_price) AS average_sale_price FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY o2.sub_category ORDER BY average_sale_price DESC;",
"Find the region with the highest average sale price": 
"SELECT o1.region, AVG(o2.sale_price) AS average_sale_price FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY o1.region ORDER BY average_sale_price DESC LIMIT 1;",
"Find the total profit per category": 
"SELECT o1.category, SUM(o2.sale_price - o2.cost_price) AS total_profit FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY o1.category ORDER BY total_profit DESC;",
"Determine the average discount percentage given per region": 
"SELECT o1.region, AVG(o2.discount_percent) AS average_discount_percentage FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY o1.region ORDER BY average_discount_percentage DESC;",
"Find the product category with the highest total profit": 
"SELECT o1.category, SUM(o2.sale_price - o2.cost_price) AS total_profit FROM orders1 o1 JOIN orders2 o2 ON o2.order_id = o1.order_id GROUP BY o1.category ORDER BY total_profit DESC LIMIT 1;",
"Calculate the total revenue generated per year": 
"SELECT EXTRACT(YEAR FROM o1.order_date) AS year, SUM(o2.sale_price) AS total_revenue FROM orders2 o2 JOIN orders1 o1 ON o2.order_id = o1.order_id GROUP BY year ORDER BY year DESC;"
}


# Sidebar navigation (assuming nav is defined based on the app's menu)
nav = st.sidebar.radio("Navigation", ["GUVI QUERIES", "Queries"])

# Query selection based on navigation
if nav == "GUVI QUERIES":
    st.subheader("GUVI QUERIES")
    query = st.selectbox("Select a query to visualize:", list(guvi_queries.keys()))
    selected_query_set = guvi_queries  

elif nav == "Queries":
    st.subheader("SELF QUERIES")
    query = st.selectbox("Select a query to visualize:", list(self_queries.keys()))
    selected_query_set = self_queries  

else:
    query = None
    selected_query_set = None

# Execute and visualize selected query
if query:
    result_df = run_query(selected_query_set[query])
    if result_df is not None:
        st.dataframe(result_df)
st.text("Thank you")
