import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
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
st.markdown("<h2 style='text-align: center;'> Retail-Orders-Dashboard </h2>", unsafe_allow_html=True)



self_queries ={# type: ignore
"displaying all tables": 
"SELECT * FROM orders1;",
"selecting all from orders2": 
"SELECT * FROM orders2;",
"joining order1 and order2 tables":
"SELECT * FROM orders1 AS o1 JOIN orders2 AS o2 ON o1.order_id = o2.order_id;",
"ordering cities alphabetically": 
"SELECT * FROM orders1  ORDER BY city ASC;",
"joining o1 order_id with o2 products": 
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
"ranking saleprice":# type: ignore
"SELECT order_id, quantity, sale_price, ROW_NUMBER() OVER (PARTITION BY sub_category ORDER BY sale_price DESC) AS rank FROM orders2;",
"discount by 20%":# type: ignore
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

    # Visualization based on selected query
    if query == "Find top 10 highest revenue generating products":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["product id"], result_df["total_revenue"], color='yellow')
        plt.title("Top 10 Highest Revenue Generating Products")
        plt.xlabel("Product ID")
        plt.ylabel("Total Revenue")


    elif query == "Find the top 5 cities with the highest profit margins":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["city"], result_df["total_profit"], color='blue')
        plt.title("Top 5 Cities with the Highest Profit Margins")
        plt.xlabel("City")
        plt.ylabel("Total Profit")


    elif query == "Calculate the total discount given for each category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["total_discount"], color='green')
        plt.title("Total Discount Given for Each Category")
        plt.xlabel("Category")
        plt.ylabel("Total Discount")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Find the average sale price per product category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["average_sales_price"], color='red')
        plt.title("Average Sales Price Per Product Category")
        plt.xlabel("Category")
        plt.ylabel("Average Sales Price")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Total profit per category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["total_profit"], color='violet')
        plt.title("Total Profit Per Category")
        plt.xlabel("Category")
        plt.ylabel("Total Profit")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Top 3 segments with the highest quantity of orders":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["highest_quantity"], color='magenta')
        plt.title("Top 3 Segments with the Highest Quantity of Orders")
        plt.xlabel("Category")
        plt.ylabel("Highest Quantity")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Determine the average discount percentage given per region":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["region"], result_df["avg_discount_percent"], color='salmon')
        plt.title("Average Discount Percentage Given Per Region")
        plt.xlabel("Region")
        plt.ylabel("Average Discount Percentage")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Find the product category with the highest total profit":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["total_profit"], color='orange')
        plt.title("Product Category with the Highest Total Profit")
        plt.xlabel("Category")
        plt.ylabel("Total Profit")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Calculate the total revenue generated per year":
        plt.figure(figsize=(10, 6))
        plt.plot(result_df["year"], result_df["total_revenue"], marker='o', color='blue')
        plt.title("Total Revenue Generated Per Year")
        plt.xlabel("Year")
        plt.ylabel("Total Revenue")
        st.pyplot(plt)

    elif query == "Total revenue per product category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["total_revenue"], color='lightblue')
        plt.title("Total Revenue Per Product Category")
        plt.xlabel("Category")
        plt.ylabel("Total Revenue")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Top 5 products by profit":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["sub category"], result_df["products_by_profit"], color='gold')
        plt.title("Top 5 Products by Profit")
        plt.xlabel("Sub Category")
        plt.ylabel("Profit")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Average sales price per sub category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["sub category"], result_df["avg_sales_price"], color='pink')
        plt.title("Average Sales Price Per Sub Category")
        plt.xlabel("Sub Category")
        plt.ylabel("Average Sales Price")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Total discount amount given by category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["total_discount_amount"], color='lightcoral')
        plt.title("Total Discount Amount Given by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Discount Amount")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Total orders per segment":
        st.write(f"Total Orders: {result_df['total_orders'][0]}")

    elif query == "Profit margin per city":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["city"], result_df["total_profit"], color='lightseagreen')
        plt.title("Profit Margin Per City")
        plt.xlabel("City")
        plt.ylabel("Total Profit")
        plt.xticks(rotation=90)
        st.pyplot(plt)

    elif query == "Average profit per category":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["category"], result_df["average_profit"], color='lightgray')
        plt.title("Average Profit Per Category")
        plt.xlabel("Category")
        plt.ylabel("Average Profit")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Top 3 cities by revenue":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["city"], result_df["revenue"], color='purple')
        plt.title("Top 3 Cities by Revenue")
        plt.xlabel("City")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif query == "Products with no profit":
        if not result_df.empty:
            st.write("Products with No Profit:")
            st.write(result_df)
        else:
            st.write("All products are generating profit.")

    elif query == "Top 3 countries with high sales by segment":
        plt.figure(figsize=(10, 6))
        plt.bar(result_df["country"], result_df["high_sales"], color='orange')
        plt.title("Top 3 Countries with High Sales by Segment")
        plt.xlabel("Country")
        plt.ylabel("High Sales")
        plt.xticks(rotation=45)
        st.pyplot(plt)
    


