import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page configuration
st.set_page_config(page_title="Trafficking Dashboard", page_icon="icon.png", layout="wide")

# Define styles for top navigation
st.markdown(
    """
    <style>
        .tab-container {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            margin-right: 10px;
            background-color: #f0f0f0;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            cursor: pointer;
            color: #000;
            text-decoration: none;
        }
        .tab.active {
            background-color: #4CAF50;
            color: white;
        }
        .tab:hover {
            background-color: #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Top Navigation Tabs
tabs = ["Overview", "Trafficking Over Time", "Conviction and Prosecution Rates"]
tab_urls = ["#Overview", "#TraffickingOverTime", "#ConvictionAndProsecutionRates"]

# Set default active tab
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Overview"

# Tab container
st.markdown('<div class="tab-container">', unsafe_allow_html=True)
for i, tab in enumerate(tabs):
    active_class = "active" if st.session_state["active_tab"] == tab else ""
    st.markdown(
        f'<a class="tab {active_class}" href="{tab_urls[i]}" onclick="window.location.hash=\'{tabs[i]}\'">{tab}</a>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# Track active tab
query_params = st.experimental_get_query_params()
if "Overview" in query_params:
    st.session_state["active_tab"] = "Overview"
elif "TraffickingOverTime" in query_params:
    st.session_state["active_tab"] = "Trafficking Over Time"
elif "ConvictionAndProsecutionRates" in query_params:
    st.session_state["active_tab"] = "Conviction and Prosecution Rates"

# Render content based on active tab
if st.session_state["active_tab"] == "Overview":
    # Overview Page
    st.title("Overview")

    # Row 1: Description columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div style="font-family: 'Sans';">
                <h3 style="color: navy; font-weight: 600;">Sex Trafficking</h3>
                <p style="color: black; font-weight: 300;">
                    Sex trafficking is the crime of using force, fraud or coercion to induce another individual to sell sex. 
                    Common types include escort services, pornography, illicit massage businesses, brothels, and outdoor solicitation.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Learn More (Sex Trafficking)"):
            st.write("[Visit Polaris Project](https://polarisproject.org/sex-trafficking/)")

    with col2:
        st.markdown(
            """
            <div style="font-family: 'Sans';">
                <h3 style="color: navy; font-weight: 600;">Labor Trafficking</h3>
                <p style="color: black; font-weight: 300;">
                    Labor trafficking is the crime of using force, fraud or coercion to induce another individual to work or provide service. 
                    Common types include agriculture, domestic work, restaurants, cleaning services, and carnivals.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Learn More (Labor Trafficking)"):
            st.write("[Visit Polaris Project](https://polarisproject.org/labor-trafficking/)")

    # Row 2: Interactive map and controls
    st.markdown("### Detected Trafficking Victims")
    map_col, controls_col = st.columns([4, 1])

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
        st.write("Legend: Placeholder for legend details.")
        
        # Bar chart for top 5 countries
        st.write("Bar Chart Placeholder")  # Replace with actual bar chart logic

elif st.session_state["active_tab"] == "Trafficking Over Time":
    # Trafficking Over Time Page
    st.title("Trafficking Over Time")
    st.write("Content for this page will go here.")

elif st.session_state["active_tab"] == "Conviction and Prosecution Rates":
    # Conviction and Prosecution Rates Page
    st.title("Conviction and Prosecution Rates")
    st.write("Content for this page will go here.")
