import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timezone, timedelta
import os

def size_to_mb(x):
    try:
        if pd.isna(x) or x == 'Varies with device':
            return None
        x = x.lower().replace('m','').replace('k','')
        if 'k' in x:
            return float(x.replace('k','')) / 1024
        return float(x)
    except:
        return None

st.set_page_config(page_title="Google Play Store Bubble Chart", layout="wide")
st.sidebar.title("Filters")
test_mode = st.sidebar.checkbox("Test Mode (show chart anytime)", value=True)

data_file = os.path.join("data", "googleplaystore.csv")

if not os.path.exists(data_file):
    st.error("CSV file not found. Make sure 'googleplaystore.csv' is inside the 'data' folder.")
    st.stop()

df = pd.read_csv(data_file)

if df.empty:
    st.error("CSV file is empty. Check the file content.")
    st.stop()

df = df.dropna(subset=['App','Category','Rating','Installs','Size'])


df = df[~df['App'].str.contains('S', case=False, na=False)]


translation_map = {
    'Beauty': 'सौंदर्य', 
    'Business': 'வியாபாரம்', 
    'Dating': 'Dating_DE'
}
df['Category_Translated'] = df['Category'].replace(translation_map)


df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(float)
df['Size_MB'] = df['Size'].apply(size_to_mb)


df = df.dropna(subset=['Rating','Reviews','Installs','Size_MB'])




all_categories = df['Category_Translated'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", all_categories, default=list(all_categories))

df_filtered = df[df['Category_Translated'].isin(selected_categories)]

df_filtered = df_filtered[(df_filtered['Rating'] > 3.0) & (df_filtered['Reviews'] > 50) & (df_filtered['Installs'] > 50000)]

st.title("Google Play Store Bubble Chart")


now_utc = datetime.now(timezone.utc)
now_ist = now_utc + timedelta(hours=5, minutes=30)
current_hour_ist = now_ist.hour

if test_mode or (17 <= current_hour_ist <= 19):
    if df_filtered.empty:
        st.warning("No apps match the selected filters. Adjust sidebar options.")
    else:

        fig = px.scatter(
            df_filtered,
            x='Size_MB',
            y='Rating',
            size='Installs',
            color='Category_Translated',

            hover_name='App',
            size_max=60,
            title="App Size vs Rating (Bubble size = Installs)"
        )

        fig.update_layout(
            xaxis_title="App Size (MB)",
            yaxis_title="Average Rating",
            legend_title="Category",
            hovermode="closest"
        )
        
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"Graph available only between 5 PM and 7 PM IST. Current IST hour: {current_hour_ist}")
