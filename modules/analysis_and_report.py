import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.benchmarks import benchmarks


def analysis_and_report():
    if "df" not in st.session_state:
        st.warning("Please upload a dataset in the campaign section before searching by metrics.")
        return

    df = st.session_state["df"] #to retrieve the dataframe from session state

    st.subheader("Individual Ad Report & Analysis 🚀")

    # Select Ad
    selection = st.number_input("Select an ad by entering its number:", min_value=1, max_value=len(df), step=1)
    ad_data = df.iloc[selection - 1]

    #key Metrics
    st.markdown("### Key Metrics Summary 🔑")
    key_metrics = ["Impressions", "Clicks", "CTR (%)", "Conversions", "Spend ($)", "Cost per Click ($)", "Conversion Rate (%)"]
    for metric in key_metrics:
        if metric in ad_data:
            st.write(f"**{metric}:** {ad_data[metric]}")

    #performance Classification
    st.markdown("### Performance Classification 🎯")
    ad_points = 0
    total_metrics = len(benchmarks)

    analysis_details = []
    scores = []
    metrics = list(benchmarks.keys())

    for key, value in benchmarks.items():
        if key in ad_data:
            if key in ["CTR (%)", "Conversion Rate (%)"]:
                meets_benchmark = ad_data[key] >= value
            elif key in ["Cost per Click ($)", "Cost per Conversion ($)", "Cost per Lead ($)"]:
                meets_benchmark = ad_data[key] <= value
            else:
                meets_benchmark = ad_data[key] > value

            # Scoring and details
            scores.append(ad_data[key] / value if meets_benchmark else value / ad_data[key])
            if meets_benchmark:
                analysis_details.append(f"✅ **{key}**: {ad_data[key]} (Meets benchmark)")
                ad_points += 1
            else:
                deviation = abs(ad_data[key] - value)
                analysis_details.append(
                    f"❌ **{key}**: {ad_data[key]} (Fails benchmark by {deviation})"
                )

    # Display Analysis Details
    st.markdown("### Detailed Analysis 📋")
    for detail in analysis_details:
        st.markdown(detail)

    # Performance Score
    performance_score = (ad_points / total_metrics) * 100
    st.write(f"### Ad Score: **{performance_score:.2f}%**")

    # Recommendations
    st.markdown("### Recommendations 💡")
    if performance_score >= 80:
        st.success("This is a winning ad. Keep running it for optimal results!")
    elif 50 <= performance_score < 80:
        st.info("This ad has potential. Consider tweaking metrics to improve performance.")
    else:
        st.error("This ad is underperforming. Revisit your ad strategy and benchmarks.")

    #visualization by using 4 differnt charts
    chart_type = st.selectbox(
        "Select chart type to visualize performance:",
        options=["Lollipop Chart", "Bar Chart", "Spider Chart", "Line Chart"]
    )

    # Data for charts
    chart_data = pd.DataFrame({
        "Metric": metrics,
        "Ad Value": [ad_data.get(metric, 0) for metric in metrics],
        "Benchmark": [benchmarks.get(metric, 0) for metric in metrics],
    })

    if chart_type == "Lollipop Chart":
        st.markdown("### Ad Performance Lollipop Chart 📊")
        fig = go.Figure()

        #lollipop for Ad Values
        fig.add_trace(go.Scatter(
            x=chart_data["Ad Value"],
            y=chart_data["Metric"],
            mode="markers+lines",
            name="Ad Value",
            marker=dict(size=10, color='blue', line=dict(color='black', width=1)),
            line=dict(width=2, color='blue'),
        ))

        #lollipop for Benchmark Values
        fig.add_trace(go.Scatter(
            x=chart_data["Benchmark"],
            y=chart_data["Metric"],
            mode="markers+lines",
            name="Benchmark",
            marker=dict(size=10, color='red', line=dict(color='black', width=1)),
            line=dict(width=2, color='red'),
        ))

        # Layout settings for Lollipop chart
        fig.update_layout(
            title="Ad Performance vs Benchmark (Lollipop Chart)",
            xaxis=dict(title="Performance Value", showgrid=True, zeroline=False),
            yaxis=dict(title="Metric", showgrid=False, zeroline=False),
            showlegend=True,
        )

        st.plotly_chart(fig)

    elif chart_type == "Bar Chart":
        st.markdown("### Ad Performance Bar Chart 📊")
        fig = px.bar(
            chart_data,
            x="Metric",
            y=["Ad Value", "Benchmark"],
            barmode="group",
            title="Ad Performance vs Benchmark (Bar Chart)",
            labels={"value": "Performance Value", "Metric": "Metric"}
        )
        st.plotly_chart(fig)

    elif chart_type == "Spider Chart":
        st.markdown("### Ad Performance vs Benchmark (Spider Chart) 📊")

        fig = go.Figure()

        #add trace for Ad Values (Ad Performance)
        fig.add_trace(go.Scatterpolar(
            r=chart_data["Ad Value"],
            theta=chart_data["Metric"],
            fill='toself',
            name="Ad Value",
            line=dict(color='blue'), 
        ))

        #add trace for Benchmark Values
        fig.add_trace(go.Scatterpolar(
            r=chart_data["Benchmark"],
            theta=chart_data["Metric"],
            fill='toself',
            name="Benchmark",
            line=dict(color='red'),
        ))

        #layout settings for Spider chart
        fig.update_layout(
            title="Ad Performance vs Benchmark (Spider Chart)",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(chart_data["Ad Value"].max(), chart_data["Benchmark"].max())],
                ),
            ),
            showlegend=True,
        )

        st.plotly_chart(fig)

    elif chart_type == "Line Chart":
        st.markdown("### Ad Performance vs Benchmark (Line Chart) 📊")
        fig = go.Figure()

        #line chart for Ad Values
        fig.add_trace(go.Scatter(
            x=chart_data["Metric"],
            y=chart_data["Ad Value"],
            mode='lines+markers',
            name="Ad Value",
            line=dict(color='blue', width=2),
        ))

        #line chart for Benchmark Values
        fig.add_trace(go.Scatter(
            x=chart_data["Metric"],
            y=chart_data["Benchmark"],
            mode='lines+markers',
            name="Benchmark",
            line=dict(color='red', width=2),
        ))

        #layout settings for Line chart
        fig.update_layout(
            title="Ad Performance vs Benchmark (Line Chart)",
            xaxis=dict(
                title="Metric",
                showgrid=True,
            ),
            yaxis=dict(
                title="Performance Value",
                showgrid=True,
            ),
            showlegend=True,
        )

        st.plotly_chart(fig)
