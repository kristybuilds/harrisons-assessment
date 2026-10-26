def get_unique_values(orders, key):
    #extracts alphabetized unique values for dropdown
    unique_values = set(str(order.get(key, "")) for order in orders if order.get(key))
    return ['All'] + sorted(list(unique_values))

def filter_orders(orders, search_query, selected_branch, selected_status):
    #filters the list of dictionaries based on user input
    filtered = []
    search_query = search_query.lower()

    for order in orders:
        #extracts from API
        sales_id = str(order.get("SalesId", "")).lower()
        customer = str(order.get("SalesName", "")).lower()
        branch = str(order.get("SalesDistrictDescription", ""))
        status = str(order.get("SalesStatus", ""))

        #check conditions
        matches_search = (search_query in sales_id) or (search_query in customer)
        matches_branch = (selected_branch == "All") or (branch == selected_branch)
        matches_status = (selected_status == "All") or (status == selected_status)

        #append if all condition pass
        if matches_search and matches_branch and matches_status:
            filtered.append(order)

    return filtered

def calculate_metrics(filtered_orders):
    #calculates totals for the dashboard
    total_orders = len(filtered_orders)

    #uses HAR_TotalSOAmount for the revenue calculation
    total_value = sum(float(order.get("HAR_TotalSOAmount", 0.0)) for order in filtered_orders)

    #count open/pending status
    open_pending = sum(1 for o in filtered_orders if str(o.get("SalesStatus", "")).lower() in ["open order", "pending", "open"])

    #count cancelled
    cancelled = sum(1 for o in filtered_orders if str(o.get("SalesStatus", "")).lower() in ["cancelled"])

    #count completed
    completed = sum(1 for o in filtered_orders if str(o.get("SalesStatus", "")).lower() in ["invoiced", "delivered", "completed"])

    return total_orders, total_value, open_pending, cancelled, completed