import os
import streamlit as st
from dotenv import load_dotenv
from api import fetch_order_data
from logic import get_unique_values, filter_orders, calculate_metrics

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="Order Dashboard", layout="wide")

if not API_URL or not API_KEY:
    st.error("Critical Error: API_URL or API_KEY is missing from the .env file.")
    st.stop()

st.title("Sales Order Monitoring")

with st.spinner("Fetching order data..."):
    orders, error = fetch_order_data(API_URL, API_KEY)
    if error:
        st.error(f"Connection Error: {error}")
    elif not orders:
        st.warning("No data found.")
    else:
        branches = get_unique_values(orders, "SalesDistrictDescription")
        status = get_unique_values(orders, "SalesStatus")

        st.sidebar.header("Search & Filters")
        search_query = st.sidebar.text_input("Search Order ID or Customer Name")
        selected_branch = st.sidebar.selectbox("District", branches)
        selected_status = st.sidebar.selectbox("Status", status)

        filter_data = filter_orders(orders, search_query, selected_branch, selected_status)
        total_orders, total_values, open_pending, cancelled, completed = calculate_metrics(filter_data)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Orders", f"{total_orders:,}")
        col2.metric("Open / Pending", f"{open_pending:,}")
        col3.metric("Completed / Invoiced / Delivered", f"{completed:,}")
        col4.metric("Cancelled", f"{cancelled:,}")
        col5.metric("Total Value", f"RM{total_values:,.2f}")

        st.markdown("---")

        #render data table
        if not filter_data:
            st.info("No records match your current filters.")
        else:
            display_data = []
            for order in filter_data:
                # Isolate the date (YYYY-MM-DD) from the ISO timestamp string
                raw_date = str(order.get("CreatedDateTime1", ""))
                clean_date = raw_date[:10] if raw_date else "N/A"
                
                display_data.append({
                    "Order Number": order.get("SalesId", ""),
                    "Customer": order.get("SalesName", ""),
                    "Branch/Site": order.get("SalesDistrictDescription", ""),
                    "Order Date": clean_date,
                    "Status": order.get("SalesStatus", ""),
                    "Amount": order.get("HAR_TotalSOAmount", 0.0)
                })
            st.dataframe(display_data, use_container_width=True)