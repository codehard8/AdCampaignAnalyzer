import streamlit as st
import pandas as pd
import plotly.express as px
from modules.benchmarks import benchmarks


def search_by_metric():
    if "df" not in st.session_state:
        st.warning("Please upload a dataset in the campaign section before searching by metrics.")
        return

    df = st.session_state["df"]#to retrieve the dataframe from session state

    st.subheader("Search Ads by Metrics 📊")
    
    #for metric selection
    metric = st.selectbox(
        "Select a metric to analyze:",
        [
            "Impressions",
            "Clicks",
            "CTR (%)",
            "Conversions",
            "Conversion Rate (%)",
            "Spend ($)",
            "Cost per Click ($)",
            "Cost per Conversion ($)",
            "Cost per Lead ($)",
        ],
    )
    
    #to filter ads by range
    min_value = int(df[metric].min())
    max_value = int(df[metric].max())
    user_range = st.slider(
        f"Filter ads by {metric} range:",
        min_value=min_value,
        max_value=max_value,
        value=(min_value, max_value),
    )
    
    #to filter the dataset
    filtered_data = df[(df[metric] >= user_range[0]) & (df[metric] <= user_range[1])]
    st.write(f"Filtered Ads by {metric} between {user_range[0]} and {user_range[1]}:")
    st.dataframe(filtered_data)
    
    # AI-powered insights
    benchmark_value = benchmarks.get(metric, None)
    if benchmark_value:
        above_benchmark = filtered_data[filtered_data[metric] >= benchmark_value]
        below_benchmark = filtered_data[filtered_data[metric] < benchmark_value]
        
        st.markdown("### AI Insights 🤖")
        st.write(f"Benchmark for **{metric}**: {benchmark_value}")
        
        st.success(f"Number of ads meeting/exceeding benchmark: {len(above_benchmark)}")
        st.error(f"Number of ads below benchmark: {len(below_benchmark)}")
        
        # Visualize filtered ads and benchmarks
        fig = px.bar(
            filtered_data,
            x="Ad Name",
            y=metric,
            color=(filtered_data[metric] >= benchmark_value).map({True: "Above Benchmark", False: "Below Benchmark"}),
            title=f"Performance of Ads Based on {metric}",
            labels={"color": "Performance"},
        )
        st.plotly_chart(fig)
    
    #highlight top and bottom performers
    if not filtered_data.empty:
        top_ad = filtered_data.loc[filtered_data[metric].idxmax()]
        bottom_ad = filtered_data.loc[filtered_data[metric].idxmin()]
        
        st.markdown("### Top Performer 🏆")
        st.write(f"**Ad Name**: {top_ad['Ad Name']}")
        st.write(f"**{metric}**: {top_ad[metric]}")
        
        st.markdown("### Bottom Performer 💔")
        st.write(f"**Ad Name**: {bottom_ad['Ad Name']}")
        st.write(f"**{metric}**: {bottom_ad[metric]}")
    else:
        st.warning("No ads match the selected range. Try adjusting the filter.")