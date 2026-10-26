# Sales Order Monitoring Dashboard

A responsive web application built with **Python** and **Streamlit** to monitor, filter, and analyze sales order data fetched from a secure, paginated REST API.

---

## 🚀 Live Demo
* **Public URL:** [https://sales-order-monitoring-harrisons-assessment.streamlit.app]

---

## 📂 Project Architecture & API Integration

The codebase follows a clean, decoupled architecture separating the UI, API data retrieval, and business logic:

* **`app.py` (Presentation Layer):** Built with Streamlit. Handles the responsive layout, KPI metric cards, sidebar filters, and renders a clean, restricted data table complying with exact assessment requirements.
* **`api.py` (Data Access Layer):** Manages secure HTTP requests using the `x-assessment-key` header, handles automated pagination looping (`pageSize` and `totalPages`), incorporates error handling, and utilizes `@st.cache_data` for performance optimization.
* **`logic.py` (Business Logic Layer):** Pure Python module handling multi-criteria filtering, unique value extraction, and KPI metric calculations (Total Orders, Open/Pending, Completed/Invoiced/Delivered, Cancelled, and Total Revenue).
* **`test_logic.py` (Testing Suite):** Comprehensive unit tests built using `pytest` to validate core business logic and metric accuracy.

---

## 🛠️ Required Data Columns Implemented
The UI data table explicitly displays only the required assessment fields:
1. **Order Number** (`SalesId`)
2. **Customer** (`SalesName`)
3. **Branch/Site** (`SalesDistrictDescription`)
4. **Order Date** (`CreatedDateTime1` - cleanly formatted to `YYYY-MM-DD`)
5. **Status** (`SalesStatus`)
6. **Amount** (`HAR_TotalSOAmount`)

---

## ⚙️ Installation & Local Run Notes

### Prerequisites
* Python 3.9 or higher installed on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/kristybuilds/harrisons-assessment.git)
cd harrisons-assessment
```

### 2. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure Environment Variables
Create a .env file in the root directory and add your assessment credentials:
API_URL=your_provided_api_url_here
API_KEY=your_provided_assessment_key_here

### 5. Launch the Web Application
streamlit run app.py
