# HealthKart Influencer Dashboard

This is an **interactive Streamlit dashboard** to track influencer campaign performance, ROAS, payouts, and insights.

## ✅ Features
- Upload real-world CSV files or use sample data
- Track performance of influencers and campaigns
- Calculate **ROI** and **incremental ROAS**
- Filters: Brand, Product, Influencer, Platform
- Visualizations: Bar charts, Pie charts, ROAS analysis
- Downloadable insights (TXT & PDF)
- Clean UI with a professional light theme

## 📂 Project Structure
healthkart_dashboard/
│── dashboard.py # Streamlit App
│── influencers.csv # Sample influencers data
│── posts.csv # Sample posts data
│── tracking_data.csv # Sample tracking data
│── payouts.csv # Sample payouts data
│── README.md
│── requirements.txt

## ✅ How to Run
1. Clone the repo:
git clone https://github.com/dishapatil2003/healthkart-influencer-dashboard.git
cd healthkart-influencer-dashboard

cpp
Copy
Edit

2. Create a virtual environment:
python -m venv venv
venv\Scripts\activate # Windows

markdown
Copy
Edit

3. Install dependencies:
pip install -r requirements.txt

markdown
Copy
Edit

4. Run the app:
streamlit run dashboard.py
## ✅ Deployment
Deployed using **Streamlit Cloud**.