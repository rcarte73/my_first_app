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

# Sidebar logo
st.sidebar.image("icon.png", use_container_width=True)

# Sidebar radio buttons
selected_tab = st.sidebar.radio(
    "",
    options=["Overview", "Trafficking Over Time", "Conviction and Prosecution Rates"],
)

# Load the data
file_path = "data_glotip.xlsx"  # Ensure this is the correct path to your data file
data = pd.read_excel(file_path, sheet_name="data_glotip_1")

# Prepare data for the map
data['txtVALUE'] = pd.to_numeric(data['txtVALUE'], errors='coerce')  # Ensure numeric values

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
            color_continuous_scale="oranges",  # Use the predefined 'oranges' colorscale
            labels={"txtVALUE": "Victims"}
        )
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
            title=None  # Remove the "undefined" title
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Trafficking Over Time":
    # Header image
    st.image("header2.jpg", use_container_width=True)

    st.title("Trafficking Over Time: United States")

    # Filter data for the United States
    us_data = data[data["Country"] == "United States"]

    # Metrics Section
    total_victims = us_data['txtVALUE'].sum()
    total_by_gender = us_data.groupby('Sex')['txtVALUE'].sum()
    total_by_age = us_data.groupby('Age')['txtVALUE'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Victims", f"{total_victims:,}")
    with col2:
        st.metric("Victims by Gender", ", ".join([f"{k}: {v:,}" for k, v in total_by_gender.items()]))
    with col3:
        st.metric("Victims by Age", ", ".join([f"{k}: {v:,}" for k, v in total_by_age.items()]))

    # Tabs for analysis
    tab = st.radio("Analysis Type", ["By Gender", "By Age Group"])

    # Year slider
    min_year, max_year = int(us_data['Year'].min()), int(us_data['Year'].max())
    selected_years = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    # Filter data by selected years
    filtered_data = us_data[(us_data['Year'] >= selected_years[0]) & (us_data['Year'] <= selected_years[1])]

    # Visualization
    if tab == "By Gender":
        # Group data by gender and year
        gender_data = filtered_data[filtered_data['Sex'].notna()].groupby(['Year', 'Sex'], as_index=False)['txtVALUE'].sum()
        fig = px.line(
            gender_data,
            x="Year",
            y="txtVALUE",
            color="Sex",
            labels={"txtVALUE": "Victims", "Sex": "Gender"},
            title="Trafficking Trends by Gender in the US"
        )
    else:
        # Group data by age and year
        age_data = filtered_data[filtered_data['Age'].notna()].groupby(['Year', 'Age'], as_index=False)['txtVALUE'].sum()
        fig = px.line(
            age_data,
            x="Year",
            y="txtVALUE",
            color="Age",
            labels={"txtVALUE": "Victims", "Age": "Age Group"},
            title="Trafficking Trends by Age Group in the US"
        )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
