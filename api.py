import requests
import streamlit as st

@st.cache_data(ttl=300)
def fetch_order_data(API_URL, API_KEY):
    all_orders = []
    current_page = 1
    total_pages = 1

    headers = {
        "x-assessment-key": API_KEY
    }

    try:
        while current_page <= total_pages:
            #set max page size allowed#
            print(f"Fetching page {current_page} of {total_pages}...")

            params = {
                "page": current_page,
                "pageSize": 100
            }

            response = requests.get(API_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            raw_json = response.json()

            if not isinstance(raw_json, dict):
                return [], "API Data Error: Expected a JSON object."

            total_pages = raw_json.get("totalPages", 1)
            page_data = raw_json.get("data", [])

            if isinstance(page_data, list):
                all_orders.extend(page_data)
            elif isinstance(page_data, dict):
                all_orders.append(page_data)

            current_page += 1

            if current_page > 50:
                print("Safety limit reached. Stopping loop.")
                break

        return all_orders, None

    except requests.exceptions.RequestException as e:
        return None, f"Network Error: {str(e)}"
    except ValueError:
        return None, "Data Error: API did not return valid JSON."