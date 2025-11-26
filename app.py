import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

import Task1_Grouped_Bar_Chart
import Task2_Scatter_Chart
import Task3_Donut_Chart
import Task4_Histogram
import Task5_Bubble_Chart
import Task6_Stacked_Area

st.set_page_config(page_title="Google Play Store Analytics", layout="wide")
st.title("Google Play Store Analytics Dashboard")
st.sidebar.title("Navigation")

page = st.sidebar.radio("Select Task", [
    "Task 1 – Grouped Bar Chart",
    "Task 2 – Scatter Chart",
    "Task 3 – Donut Chart",
    "Task 4 – Histogram",
    "Task 5 – Bubble Chart",
    "Task 6 – Stacked Area Chart"
])

if page == "Task 1 – Grouped Bar Chart":
    Task1_Grouped_Bar_Chart.main()
elif page == "Task 2 – Scatter Chart":
    Task2_Scatter_Chart.main()
elif page == "Task 3 – Donut Chart":
    Task3_Donut_Chart.main()
elif page == "Task 4 – Histogram":
    Task4_Histogram.main()
elif page == "Task 5 – Bubble Chart":
    Task5_Bubble_Chart.main()
elif page == "Task 6 – Stacked Area Chart":
    Task6_Stacked_Area.main()
