from logic import get_unique_values, filter_orders, calculate_metrics

MOCK_ORDERS = [
    {"SalesId": "SO-MOCK-001", "SalesName": "Siti Mart Sdn Bhd", "SalesDistrictDescription": "Lahad Datu", "SalesStatus": "Open order", "HAR_TotalSOAmount": 100.0},
    {"SalesId": "SO-MOCK-002", "SalesName": "Ahmad Distribution", "SalesDistrictDescription": "Sandakan", "SalesStatus": "Invoiced", "HAR_TotalSOAmount": 250.50},
    {"SalesId": "SO-MOCK-003", "SalesName": "Priya Enterprise", "SalesDistrictDescription": "Lahad Datu", "SalesStatus": "Pending", "HAR_TotalSOAmount": 50.0},
    {"SalesId": "SO-MOCK-004", "SalesName": "Wei Holdings", "SalesDistrictDescription": "Tawau", "SalesStatus": "Delivered", "HAR_TotalSOAmount": 600.0},
    {"SalesId": "SO-MOCK-005", "SalesName": "Batal Sdn Bhd", "SalesDistrictDescription": "Tawau", "SalesStatus": "Cancelled", "HAR_TotalSOAmount": 0.0}
]

def test_get_unique_options():
    #verifies dropdown values are extracted, sorted alphabetically and unique
    districts = get_unique_values(MOCK_ORDERS, "SalesDistrictDescription")

    assert districts == ["All", "Lahad Datu", "Sandakan", "Tawau"]

def test_filter_orders_by_district():
        result = filter_orders(MOCK_ORDERS, search_query="", selected_branch="Lahad Datu", selected_status="All")

        assert len(result) == 2
        assert result[0]["SalesName"] == "Siti Mart Sdn Bhd"
        assert result[1]["SalesName"] == "Priya Enterprise"

def test_filter_orders_by_search():
    #verifies text search is case-insensitive and checks both SalesId and SalesName
    #searching by name
    result_name = filter_orders(MOCK_ORDERS, search_query="ahmad", selected_branch="All", selected_status="All")
    assert len(result_name) == 1
    assert result_name[0]["SalesId"] == "SO-MOCK-002"
    
    #searching by ID
    result_id = filter_orders(MOCK_ORDERS, search_query="mock-004", selected_branch="All", selected_status="All")
    assert len(result_id) == 1
    assert result_id[0]["SalesName"] == "Wei Holdings"

def test_calculate_metrics():
    #verifies the dashboard math calculates correctly based on status strings and floats
    total_orders, total_values, open_pending, cancelled, completed = calculate_metrics(MOCK_ORDERS)
    
    assert total_orders == 5
    assert total_values == 1000.50    # 100.0 + 250.50 + 50.0 + 600.0
    assert open_pending == 2        # Siti Mart (Open order), Priya (Pending)
    assert cancelled == 1           # Ahmad (Invoiced), Wei (Delivered)
    assert completed == 2             # Ahmad (Invoiced), Wei (Delivered)