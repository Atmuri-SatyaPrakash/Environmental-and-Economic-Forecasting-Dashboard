# Environmental-and-Economic-Forecasting-Dashboard
🚦 Full-stack data pipeline that connects environmental (air quality, weather) and economic data sources, performs anomaly detection and forecasting, and delivers interactive visual insights via a Flask dashboard. Built with Python, MongoDB, PostgreSQL, and machine learning models.

---

# 🌍 Air Quality & Economic Forecasting Dashboard

This project is a complete end-to-end data analytics and visualization system that brings together *environmental data* (air quality, weather) and *economic data* (GDP indicators) to deliver *interactive, real-time dashboards*. 

It uses *machine learning models* such as Isolation Forest, ARIMA, and Linear Regression to uncover hidden patterns, forecast future values, and enable informed decision-making through visual storytelling.

---

## 🎯 Project Objectives

- Integrate multi-source datasets (Open AQ, Open Meteo, World Bank)
- Automate data retrieval, storage, and transformation using APIs, MongoDB, and PostgreSQL
- Train and evaluate anomaly detection and forecasting models
- Deploy results through interactive dashboards using Flask and Plotly
- Make data insights accessible to technical and non-technical users

---

## 🧠 Key Features

✅ Real-time air quality tracking with anomaly detection using *IsolationForest*  
✅ Weather prediction using *ARIMA* time-series forecasting  
✅ Economic forecasting using *Linear Regression* on World Bank GDP data  
✅ End-to-end ETL pipeline with *MongoDB* and *PostgreSQL*  
✅ *Interactive web dashboards* via *Flask + Plotly*  

---

## 📊 Visual Outputs

Here are some of the interactive visualizations included:

- PM2.5 Anomaly Scatter Plot (Red = Anomaly, Blue = Normal)
- Temperature Forecast Line Chart
- India GDP Forecast Trend (1960–2030)
- K-Means Cluster Visuals for grouped insights

All visuals are dynamically rendered and presented through a web-based interface built using Flask.

---

## 🧱 Tech Stack

| Layer | Tools/Frameworks |
|------|------------------|
| Data Ingestion | Open AQ API, Open Meteo API, World Bank CSV |
| Storage | MongoDB (NoSQL), PostgreSQL (SQL) |
| Programming | Python (Pandas, NumPy, scikit-learn, statsmodels) |
| ML Models | IsolationForest, ARIMA, Linear Regression, K-Means |
| Visualization | Flask, Plotly, Dash |
| Environment | Jupyter Notebook, VSCode |


---

## 🚀 How to Run This Project Locally

### 📁 1. Clone the Repository
```bash
git clone https://github.com/yourusername/analytics-data-viz-project.git
cd analytics-data-viz-project
```

### 🐍 2. Create a Virtual Environment
```bash
python -m venv venv
```

- For **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- For **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 📦 3. Install the Required Dependencies
```bash
pip install -r requirements.txt
```

### 🔧 4. Run the Flask App
```bash
cd app
python flask_app.py
```

### 🌐 5. View the Dashboard

Open your browser and go to:

```
http://localhost:5000
```

---

## 🔮 Future Improvements

- 🌐 Integrate satellite and IoT-based environmental data sources  
- 🔁 Add LSTM deep learning models for time series forecasting  
- ☁️ Deploy the Flask app online via **Heroku**, **Render**, or similar platforms  
- 🎨 Enhance dashboard UX/UI using user feedback and design upgrades  

---

## 👤 Author

**Atmuri Satya Prakash**  

---

## 🤝 Acknowledgements

- [Open AQ](https://openaq.org/)  
- [Open Meteo](https://open-meteo.com/)  
- [World Bank Open Data](https://data.worldbank.org/)
```
