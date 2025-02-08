import streamlit as st
import pandas as pd

def show_campaign():
    #hero Section with Title and Background
    st.markdown(
        """
        <style>
        .hero {
            background: linear-gradient(135deg, #a0a0a0, #c0c0c0, #e0e0e0);
            color: black; /* Changed font color to black */
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .hero h1 {
            font-size: 2.5rem;
            text-align: center;
            font-weight: bold;
        }
        .hero p {
            font-size: 1.2rem;
            text-align: center;
            margin-top: 10px;
        }
        .section-title {
            font-size: 1.5rem;
            color: black;
            margin-top: 20px;
        }
        .divider {
            border: 0.5px solid #BDC3C7;
            margin: 20px 0;
        }
        </style>
        <div class="hero">
            <h1>Welcome to Ad Analysis Software</h1>
            <p>Your ultimate tool to evaluate and enhance ad campaign performance!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns([1, 2], gap="large")#for 2 columns
    with col1:
        st.image("ab.png", use_container_width=True, caption="Your Partner in Ad Success")

    with col2:
        st.subheader("Why Choose Us?")
        st.markdown(
            """
            - 🚀 **Analyze ad campaigns** with comprehensive metrics.
            - 📊 **Compare performance** with industry benchmarks.
            - 💡 **Gain actionable insights** to optimize ROI.
            - 🎨 **Visualize data** using interactive and intuitive graphs.
            """
        )
        st.markdown(#used anchored link to get to upload section
            """
            <div style="text-align: center;">
                <a href="#upload-section">
                    <button style="background: linear-gradient(135deg, #a0a0a0, #c0c0c0, #e0e0e0); color: white; border: none; 
                    padding: 10px 20px; font-size: 16px; border-radius: 5px;">
                    Get Started
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    #2 sections divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    #features Section
    st.subheader("🌟 Features Overview")
    st.markdown(
        """
        1. **Data Analysis**: Evaluate ad metrics like impressions, clicks, CTR, and conversions.
        2. **Benchmarking**: Compare against industry benchmarks to spot strengths and gaps.
        3. **Insights**: Determine the profitability of campaigns and improve decision-making.
        4. **Visualization Tools**: Uncover trends and patterns with dynamic, interactive graphs.
        """
    )

    #divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    #file Upload Section with Anchor we made before
    st.markdown('<div id="upload-section"></div>', unsafe_allow_html=True)#anchor=upload-section
    st.markdown("### 📁 Upload Your Campaign Data")
    uploaded_file = st.file_uploader(
        "Upload your campaign data in Excel format (.xlsx):",
        type=["xlsx"],
        help="Upload a valid Excel file to analyze your ad campaigns."
    )

    @st.cache_data
    def load_data(file):
        """
        Load data from the uploaded Excel file.
        """
        try:
            if file is not None:
                return pd.read_excel(file)#to read the uploaded Excel file
            else:
                return None
        except Exception as e:
            st.error("Error loading data. Please ensure the file is a valid Excel file.")
            st.stop()

    #Data Display Based on File Upload
    if uploaded_file:
        df = load_data(uploaded_file)
        st.session_state["df"] = df #saved to session state for global use
        st.success("🎉 File uploaded successfully!")
        st.dataframe(df.head(5))#display first 5 rows

    elif "df" in st.session_state:
        df = st.session_state["df"]  #to retrieve the previously uploaded dataframe
        st.info("📄 Using previously uploaded data.")
        st.dataframe(df.head(5))
    else:
        st.info("Please upload an Excel file to view and analyze your data.")

    #footer Section
    st.markdown(
        """
        <style>
        .footer {
            font-size: 0.9rem;
            text-align: center;
            margin-top: 50px;
            color: #95A5A6;
        }
        </style>
        <div class="footer">
            @hakuna matata.
        </div>
        """,
        unsafe_allow_html=True,
    )

