import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui

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

# Sidebar logo
st.sidebar.image("icon.png", use_container_width=True)

# Sidebar radio buttons
selected_tab = st.sidebar.radio(
    "",
    options=["Overview", "Trafficking Over Time", "Conviction and Prosecution Rates"],
)

# Load the data
file_path = "data_glotip.xlsx" 
data = pd.read_excel(file_path, sheet_name="data_glotip_1")

# Prepare data for the map
data['txtVALUE'] = pd.to_numeric(data['txtVALUE'], errors='coerce')

# Content rendering based on selected tab
if selected_tab == "Overview":
    # Overview Page
    st.image("header.jpg", use_container_width=True)

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

    # Interactive controls for the map
    map_col, controls_col = st.columns([4, 1])

    with controls_col:
        # Date range slider
        min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
        date_range = st.slider(
            "Select Date Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1
        )

        # Country dropdown
        country_list = ["All Countries"] + sorted(data["Country"].dropna().unique())
        selected_countries = st.multiselect(
            "Select Country/Countries",
            options=country_list,
            default="All Countries"
        )

        # Filter data by date range and selected countries
        filtered_data = data[(data['Year'] >= date_range[0]) & (data['Year'] <= date_range[1])]
        if "All Countries" not in selected_countries:
            filtered_data = filtered_data[filtered_data["Country"].isin(selected_countries)]
            
    with map_col:
        # Prepare filtered data for the map
        map_data = filtered_data.groupby('Country', as_index=False)['txtVALUE'].sum()
        fig = px.choropleth(
            map_data,
            locations="Country",
            locationmode="country names",
            color="txtVALUE",
            color_continuous_scale="oranges", 
            labels={"txtVALUE": "Victims"}
        )
        fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
        title_text="",  
        title_x=0.5  
)

        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Trafficking Over Time":
    # Header image
    st.image("header2.jpg", use_container_width=True)

    # Page content goes here (Trafficking Over Time logic)...

elif selected_tab == "Conviction and Prosecution Rates":
    # Header image
    st.image("header3.jpg", use_container_width=True)

    # Page title
    st.markdown(
        """
        <style>
            .page-title {
                font-family: 'Sans', sans-serif;
                font-size: 28px;
                font-weight: bold;
                color: navy;
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
        <div class="page-title">Convictions and Prosecution Rates</div>
        """,
        unsafe_allow_html=True,
    )

    # Create tabs
    vulnerabilities_tab, traffickers_tab, control_tab, survivors_tab = st.tabs(
        ["Vulnerabilities", "Traffickers", "Control", "Survivors"]
    )

    # Tab 1: Vulnerabilities
    with vulnerabilities_tab:
        st.markdown(
            """
            <style>
                .vulnerability-title {
                    font-family: 'Sans', sans-serif;
                    font-size: 18px;
                    font-weight: 600;
                    color: navy;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .vulnerability-body {
                    font-family: 'Sans', sans-serif;
                    font-size: 14px;
                    font-weight: 300;
                    color: black;
                    text-align: center;
                    margin-bottom: 20px;
                }
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
                    margin: 0 auto; /* Center the button */
                }
                .button-learn-more:hover {
                    background-color: navy;
                    color: white;
                }
            </style>
            <div class="vulnerability-title">Vulnerabilities</div>
            <div class="vulnerability-body">
                Certain factors increase the risk of being trafficked. These include poverty, lack of education, migration, 
                homelessness, and lack of social safety nets. Vulnerable individuals are often targeted and exploited.
            </div>
            <div style="text-align: center;">
                <a href="https://polarisproject.org/vulnerabilities" target="_blank" class="button-learn-more">Learn More</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 2: Traffickers
    with traffickers_tab:
        st.write("Content for Traffickers goes here.")  # Replace with actual content later

    # Tab 3: Control
    with control_tab:
        st.write("Content for Control goes here.")  # Replace with actual content later

    # Tab 4: Survivors
    with survivors_tab:
        st.write("Content for Survivors goes here.")  # Replace with actual content later
