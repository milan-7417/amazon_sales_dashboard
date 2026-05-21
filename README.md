# 📊 Amazon Sales Analytics Dashboard

A professional interactive sales analytics dashboard built using **Python, Plotly Dash, Pandas, and Plotly Express** to analyze Amazon sales performance. This project focuses on **data cleaning, exploratory data analysis (EDA), business insights, and interactive dashboarding**.

---

## 🚀 Live Demo

🔗 **Dashboard Link:** *(Add Plotly Cloud URL after deployment)*

---

## 📌 Project Overview

This dashboard helps analyze Amazon sales data and provides key business insights through interactive visualizations.

The project includes:

- Data Cleaning
- Exploratory Data Analysis (EDA)
- KPI Tracking
- Interactive Filters
- Business Insights Dashboard
- Deployment on Plotly Cloud

---

## 📂 Dataset Information

The dataset contains Amazon sales transaction records with information such as:

- Order Status
- Fulfilment Type
- Product Category
- Quantity Sold
- Revenue
- State-wise Shipping
- Courier Status
- Product Size
- Sales Channel

### Dataset Features

| Feature | Description |
|----------|-------------|
| Date | Order date |
| Status | Order delivery status |
| Fulfilment | Amazon / Merchant fulfilment |
| Category | Product category |
| Qty | Quantity ordered |
| Amount | Revenue generated |
| ship-state | State of shipment |
| Courier Status | Shipping progress |
| Size | Product size |
| B2B | Business order indicator |

---

## 🧹 Data Cleaning Process

The following preprocessing steps were performed:

- Removed irrelevant columns
- Handled missing values
- Converted `Date` column to datetime format
- Created new features:
  - `Year`
  - `Month`
  - `Month_num`
  - `Day`
- Removed duplicate records
- Fixed data types
- Prepared cleaned dataset for dashboard

---

## 📈 Exploratory Data Analysis (EDA)

Performed detailed EDA to understand:

### Sales Analysis
- Monthly Revenue Trend
- Revenue by Category
- Top Performing States
- Quantity Distribution

### Order Analysis
- Order Status Distribution
- Courier Performance
- Fulfilment Analysis

### Customer Insights
- Size Demand Analysis
- Cancellation Rate

---

## 🎯 Dashboard Features

### 📌 Interactive Filters
- State Filter
- Category Filter
- Status Filter
- Fulfilment Filter

### 📌 KPI Cards
- Total Revenue
- Total Orders
- Total Quantity Sold
- Average Order Value
- Cancellation Rate
- Top Category

### 📌 Interactive Visualizations
- Monthly Revenue Trend
- Order Status Distribution
- Revenue by Category
- Top States by Revenue
- Courier Performance
- Size Demand Analysis

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Libraries Used
- Dash
- Plotly
- Pandas
- NumPy
- PyArrow

### Visualization
- Plotly Express
- Plotly Graph Objects

### Deployment
- Plotly Cloud

---

## 📁 Project Structure

```bash
amazon-sales-dashboard/
│── app.py
│── requirements.txt
│── runtime.txt
│── README.md
│── .gitignore
│
├── assets/
│   └── style.css
│
├── data/
│   └── cleaned_amazon_sales.csv
│
├── notebooks/
│   └── eda.ipynb
```

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/milan-7417/amazon_sales_dashboard.git
```

Go to project directory:

```bash
cd amazon-sales-dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run dashboard:

```bash
python app.py
```

Dashboard will run on:

```text
http://127.0.0.1:8050/
```

---

## 📊 Key Business Insights

- Certain categories contribute the highest revenue.
- Some states generate significantly higher sales.
- Cancellation rate impacts business performance.
- Fulfilment method influences order outcomes.
- Revenue trends vary across months.

---

## 🔮 Future Improvements

- Add Forecasting using Machine Learning
- Add Profit Analysis
- Add Geo Map Visualizations
- Add Customer Segmentation
- Connect to Real-Time Database

---

## 👨‍💻 Author

**Milan Kumar**

- GitHub: https://github.com/milan-7417
- Kaggle: https://www.kaggle.com/raimilanbr22


---

## ⭐ If you found this project useful, give it a star!