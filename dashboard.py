import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="HealthKart Dashboard", layout="wide")

# ----------------------------
# Custom CSS for Animated Background and Cards
# ----------------------------
st.markdown("""
    <style>
    /* Animated Gradient Background */
    .main {
        background: linear-gradient(-45deg, #f8f9fc, #e0eafc, #f1f8ff, #e4ecfa);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        border-radius: 12px;
        padding: 20px;
        color: #333333;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .kpi-value {
        font-size: 28px;
        margin-top: 10px;
        font-weight: bold;
    }

    /* Insights Cards */
    .insight-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: #2c3e50;
        font-size: 16px;
    }
    .insight-title {
        font-weight: bold;
        font-size: 18px;
        color: #0073e6;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar - Data Upload or Sample
# ----------------------------
st.sidebar.image("https://healthkart.com/images/logo.png", width=150)
st.sidebar.header("📂 Data Source")
use_sample = st.sidebar.radio("Select Data Source", ["Sample Data", "Upload CSVs"])

# ----------------------------
# Load Data
# ----------------------------
if use_sample == "Sample Data":
    df_inf = pd.read_csv('influencers.csv')
    df_post = pd.read_csv('posts.csv')
    df_track = pd.read_csv('tracking_data.csv')
    df_payout = pd.read_csv('payouts.csv')
else:
    st.sidebar.subheader("Upload Your CSV Files")
    uploaded_inf = st.sidebar.file_uploader("Upload influencers.csv", type="csv")
    uploaded_post = st.sidebar.file_uploader("Upload posts.csv", type="csv")
    uploaded_track = st.sidebar.file_uploader("Upload tracking_data.csv", type="csv")
    uploaded_payout = st.sidebar.file_uploader("Upload payouts.csv", type="csv")

    if uploaded_inf and uploaded_post and uploaded_track and uploaded_payout:
        df_inf = pd.read_csv(uploaded_inf)
        df_post = pd.read_csv(uploaded_post)
        df_track = pd.read_csv(uploaded_track)
        df_payout = pd.read_csv(uploaded_payout)
    else:
        st.warning("Please upload all 4 files to proceed.")
        st.stop()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔍 Filters")
campaign = st.sidebar.selectbox("Select Campaign", df_track['campaign'].unique())
platforms = st.sidebar.multiselect("Select Platforms", df_inf['platform'].unique(), default=df_inf['platform'].unique())

filtered_inf = df_inf[df_inf['platform'].isin(platforms)]
filtered_track = df_track[(df_track['campaign'] == campaign) & (df_track['influencer_id'].isin(filtered_inf['ID']))]

# ----------------------------
# Metrics Calculation
# ----------------------------
total_revenue = filtered_track['revenue'].sum()
inf_ids = filtered_track['influencer_id'].unique()
total_payout = df_payout[df_payout['influencer_id'].isin(inf_ids)]['total_payout'].sum()
roas = total_revenue / total_payout if total_payout else 0

# Prepare ROAS DF
roas_df = filtered_track.groupby('influencer_id').agg({'revenue':'sum'}).reset_index()
roas_df = roas_df.merge(df_payout[['influencer_id','total_payout']], on='influencer_id')
roas_df['ROAS'] = roas_df['revenue'] / roas_df['total_payout']
roas_df = roas_df.merge(df_inf[['ID','name']], left_on='influencer_id', right_on='ID')

# Top influencers for table and chart
top_inf = filtered_track.groupby('influencer_id').agg({'orders':'sum','revenue':'sum'}).reset_index()
top_inf = top_inf.merge(df_inf, left_on='influencer_id', right_on='ID')
top_inf = top_inf.sort_values(by='revenue', ascending=False).head(5)

platform_data = filtered_inf['platform'].value_counts().reset_index()
platform_data.columns = ['platform', 'count']

# ----------------------------
# Tabs for Navigation
# ----------------------------
st.title("🏋 HealthKart Influencer Campaign Dashboard")
tab1, tab2, tab3 = st.tabs(["📌 Overview", "📊 Charts", "💡 Insights"])

# ----------------------------
# Tab 1: Overview
# ----------------------------
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='kpi-card'>Total Revenue<div class='kpi-value'>₹{total_revenue:,.2f}</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-card'>Total Payout<div class='kpi-value'>₹{total_payout:,.2f}</div></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-card'>ROAS<div class='kpi-value'>{roas:.2f}x</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🔥 Top Performing Influencers")
    st.dataframe(top_inf[['name', 'platform', 'category', 'revenue', 'orders']])

# ----------------------------
# Tab 2: Charts
# ----------------------------
with tab2:
    st.subheader("Charts Visualization")
    fig1 = px.bar(top_inf, x='name', y='revenue', color='platform', title="Top Influencers by Revenue",
                  text_auto='.2s', color_discrete_sequence=px.colors.qualitative.Set2)
    fig1.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(platform_data, values='count', names='platform', title="Influencer Platform Share",
                  color_discrete_sequence=px.colors.sequential.Teal)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(roas_df.sort_values('ROAS', ascending=False), x='name', y='ROAS', title="ROAS by Influencer",
                  text_auto='.2f', color_discrete_sequence=['#0073e6'])
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Tab 3: Insights
# ----------------------------
with tab3:
    st.subheader("💡 Campaign Insights")
    top_name = top_inf.iloc[0]['name'] if not top_inf.empty else "N/A"
    best_platform = platform_data.iloc[0]['platform'] if not platform_data.empty else "N/A"
    worst_roas = roas_df.sort_values('ROAS').iloc[0]['name'] if not roas_df.empty else "N/A"

    col_a, col_b, col_c = st.columns(3)
    col_a.markdown(f"<div class='insight-card'><div class='insight-title'>Top Influencer</div>{top_name}</div>", unsafe_allow_html=True)
    col_b.markdown(f"<div class='insight-card'><div class='insight-title'>Best Platform</div>{best_platform}</div>", unsafe_allow_html=True)
    col_c.markdown(f"<div class='insight-card'><div class='insight-title'>Lowest ROAS</div>{worst_roas}</div>", unsafe_allow_html=True)

    st.markdown("### 📥 Export Insights")
    if st.button("Export Top Influencers CSV"):
        top_inf.to_csv('top_influencers.csv', index=False)
        st.success("✅ Exported as top_influencers.csv")

    def create_download_link(val, filename):
        b64 = base64.b64encode(val.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📄 Download Insights</a>'

    summary_text = f"""HealthKart Campaign Insights\n
    Campaign: {campaign}\n
    Total Revenue: ₹{total_revenue:,.2f}\n
    Total Payout: ₹{total_payout:,.2f}\n
    ROAS: {roas:.2f}x\n
    Top Influencer: {top_name}\n
    Best Platform: {best_platform}\n
    Lowest ROAS Influencer: {worst_roas}\n
    Top Influencers Table:\n{top_inf[['name','platform','revenue']].to_string(index=False)}
    """
    st.markdown(create_download_link(summary_text, "campaign_insights.txt"), unsafe_allow_html=True)
