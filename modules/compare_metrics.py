import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.benchmarks import benchmarks

def compare_metrics():
    if "df" not in st.session_state:
        st.warning("Please upload a dataset in the campaign section before searching by metrics.")
        return

    df = st.session_state["df"]#to retrieve the dataframe

    st.subheader("Metric Comparison")
    st.markdown("Compare ad metrics against benchmarks and visualize them as a chart.")

    metric = st.selectbox(#select metric to compare
        "Select a metric to compare:",
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
        ]
    )

    #select ads for comparison
    selected_ads = st.multiselect(
        "Select ads to compare:",
        options=df["Ad Name"],
        default=df["Ad Name"].tolist(),  #by default: Select all ads
    )

    # Filter the data based on selected ads
    filtered_df = df[df["Ad Name"].isin(selected_ads)]
    ad_values = filtered_df[metric]
    benchmark_value = benchmarks[metric]

# for slider
    min_value = ad_values.min()
    max_value = ad_values.max()

    # Determine if the metric is an integer or float
    if metric in ["Impressions", "Clicks", "Conversions"]:
        range_min, range_max = st.slider(#integer based slider
            f"Filter {metric} values:",
            min_value=int(min_value),
            max_value=int(max_value),
            value=(int(min_value), int(max_value)),
            step=1,
        )
    else:
        range_min, range_max = st.slider(#float based slider
            f"Filter {metric} values:",
            min_value=float(min_value),
            max_value=float(max_value),
            value=(float(min_value), float(max_value)),
            step=0.1,
        )

    #to filter data based on the selected range
    filtered_df = filtered_df[(ad_values >= range_min) & (ad_values <= range_max)]
    ad_values = filtered_df[metric]  #update filtered values

    # Prepare the comparison DataFrame
    comparison_df = pd.DataFrame({
        "Ad Name": filtered_df["Ad Name"],
        "Ad Value": ad_values,
        "Benchmark": [benchmark_value] * len(filtered_df),
        "Difference (%)": ((ad_values - benchmark_value) / benchmark_value * 100).round(2),
    })

    # Add performance flag
    comparison_df["Performance"] = np.where(
        (
            ((metric in ["Cost per Click ($)", "Cost per Conversion ($)", "Cost per Lead ($)"]) & (ad_values <= benchmark_value)) |
            ((metric not in ["Cost per Click ($)", "Cost per Conversion ($)", "Cost per Lead ($)"]) & (ad_values >= benchmark_value))
        ),
        "Meets Benchmark",
        "Below Benchmark"
    )

    # Sort ads by performance
    comparison_df = comparison_df.sort_values("Ad Value", ascending=False)

    # Interactive Plotly Chart with Dropdown for Chart Type
    chart_type = st.radio("Choose chart type:", ["Bar Chart", "Line Chart"])
    if chart_type == "Bar Chart":
        fig = px.bar(
            comparison_df,
            x="Ad Name",
            y="Ad Value",
            color="Performance",
            text="Difference (%)",
            title=f"Comparison of {metric} with Benchmark",
            labels={"Ad Value": metric, "Performance": "Status"},
            hover_data=["Benchmark", "Difference (%)"],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
    elif chart_type == "Line Chart":
        fig = px.line(
            comparison_df,
            x="Ad Name",
            y=["Ad Value", "Benchmark"],
            title=f"Comparison of {metric} with Benchmark",
            labels={"value": metric, "variable": "Type"},
            markers=True,
        )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

