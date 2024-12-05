import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page configuration
st.set_page_config(page_title="Trafficking Dashboard", page_icon="icon.png", layout="wide")

# Sidebar and page styling
st.markdown(
    """
    <style>
        /* Main page background color */
        .main {
            background-color: #f0f0f0;
        }

        /* Sidebar background color */
        .css-1d391kg {
            background-color: white !important;
        }

        /* Sidebar text styling */
        .css-1d391kg, .css-qbe2hs, .css-h5rgaw {
            color: navy !important;
            font-family: 'Sans', sans-serif !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
st.sidebar.image("icon.png", use_container_width=True)
tabs = ["Overview", "Trafficking Over Time", "Conviction and Prosecution Rates"]
selected_tab = st.sidebar.radio("Navigation", tabs)

# Preserve user selections across pages
if "date_range" not in st.session_state:
    st.session_state["date_range"] = None
if "selected_country" not in st.session_state:
    st.session_state["selected_country"] = None

# Content rendering based on selected tab
if selected_tab == "Overview":
    # Overview Page

    # Display the header image using st.image
    st.image("header.jpg", use_column_width=True)

    # Row 1: Description columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <style>
                .button-learn-more {
                    background-color: #f0f0f0;
                    color: black;
                    padding: 10px 15px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    border-radius: 5px;
                    font-size: 16px;
                    font-family: 'Sans', sans-serif;
                    border: 1px solid navy;
                    cursor: pointer;
                }
                .button-learn-more:hover {
                    background-color: navy;
                    color: white;
                }
            </style>
            <div style="font-family: 'Sans'; text-align: center;">
                <h3 style="color: navy; font-weight: 600;">Sex Trafficking</h3>
                <p style="color: black; font-weight: 300;">
                    Sex trafficking is the crime of using force, fraud or coercion to induce another individual to sell sex. 
                    Common types include escort services, pornography, illicit massage businesses, brothels, and outdoor solicitation.
                </p>
                <a href="https://polarisproject.org/sex-trafficking/" target="_blank" class="button-learn-more">Learn More</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="font-family: 'Sans'; text-align: center;">
                <h3 style="color: navy; font-weight: 600;">Labor Trafficking</h3>
                <p style="color: black; font-weight: 300;">
                    Labor trafficking is the crime of using force, fraud or coercion to induce another individual to work or provide service. 
                    Common types include agriculture, domestic work, restaurants, cleaning services, and carnivals.
                </p>
                <a href="https://polarisproject.org/labor-trafficking/" target="_blank" class="button-learn-more">Learn More</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Row 2: Interactive map and controls
    st.markdown(
        """
        <style>
            .section-title {
                font-family: 'Sans', sans-serif;
                font-size: 28px;
                font-weight: bold;
                color: navy;
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="section-title">Detected Trafficking Victims</div>', unsafe_allow_html=True)

    map_col, controls_col = st.columns([4, 1])  # 80/20 split

    with map_col:
        st.write("Map Visualization Here (Placeholder)")  # Replace with actual map logic

    with controls_col:
        # Date range slider
        date_range = st.slider(
            "Select Date Range",
            min_value=2000,
            max_value=2021,
            value=(2005, 2015),
            step=1
        )
        st.session_state["date_range"] = date_range

        # Country dropdown
        country_list = ["All Countries", "USA", "Canada", "UK"]  # Replace with actual list from data
        selected_country = st.selectbox("Select a Country", country_list)
        st.session_state["selected_country"] = selected_country

        # Legend placeholder
        st.markdown("**Legend:**")
        st.write("Placeholder for legend details.")  # Replace with actual legend logic

        # Bar chart for top 5 countries
        st.markdown("### Top 5 Countries")
        st.write("Bar Chart Placeholder")  # Replace with actual bar chart logic

elif selected_tab == "Trafficking Over Time":
    st.title("Trafficking Over Time")
    st.write("Content for this page will go here.")

elif selected_tab == "Conviction and Prosecution Rates":
    st.title("Conviction and Prosecution Rates")
    st.write("Content for this page will go here.")
