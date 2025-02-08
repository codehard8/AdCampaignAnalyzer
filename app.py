import streamlit as st
from modules.show_campaign import show_campaign
from modules.search_by_metric import search_by_metric
from modules.analysis_and_report import analysis_and_report
from modules.compare_metrics import compare_metrics

st.title("Ad Analysis Software for Kitchen and Bathroom Remodeling Businesses")

#navigation menu
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Search by Metric", "Analysis and Report", "Compare Metrics"]
)

if menu == "Home":
    show_campaign()
elif menu == "Search by Metric":
    search_by_metric()
elif menu == "Analysis and Report":
    analysis_and_report()
elif menu == "Compare Metrics":
    compare_metrics()
