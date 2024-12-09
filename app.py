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

    # Filter data for the United States of America
    data["Country"] = data["Country"].str.strip().str.title()  # Normalize Country column
    us_data = data[data["Country"] == "United States Of America"]

    if us_data.empty:
        st.warning("No data available for the United States of America in the selected dataset.")
    else:
        # Clean the Year column
        us_data = us_data.dropna(subset=["Year"])  # Drop rows with NaN in Year
        us_data["Year"] = pd.to_numeric(us_data["Year"], errors="coerce")  # Convert safely
        us_data = us_data.dropna(subset=["Year"])  # Drop remaining invalid rows

        # Year slider
        min_year, max_year = int(us_data['Year'].min()), int(us_data['Year'].max())
        selected_years = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
        )

        # Filter data by selected years
        filtered_data = us_data[(us_data['Year'] >= selected_years[0]) & (us_data['Year'] <= selected_years[1])]

        # Dynamic title
        st.markdown(
            f"""
            <style>
                .page-title {{
                    font-family: 'Sans', sans-serif;
                    font-size: 28px;
                    font-weight: bold;
                    color: navy;
                    text-align: center;
                    margin-bottom: 20px;
                }}
            </style>
            <div class="page-title">Trafficking Over Time: U.S. ({selected_years[0]} - {selected_years[1]})</div>
            """,
            unsafe_allow_html=True,
        )

        # Prepare dynamic metrics
        total_victims = int(filtered_data['txtVALUE'].sum())
        total_by_gender = filtered_data.groupby('Sex')['txtVALUE'].sum()
        total_by_gender = total_by_gender[["Female", "Male"]] if "Female" in total_by_gender and "Male" in total_by_gender else total_by_gender
        total_by_age = filtered_data.groupby('Age')['txtVALUE'].sum()
        total_by_age = {
            "Minors": int(total_by_age.get("0 to 17 years", 0)),
            "Adults": int(total_by_age.get("18 years or over", 0)),
        }

        metrics = [
            {"title": "Total Victims", "content": f"{total_victims:,}", "description": "Detected victims"},
            {
                "title": "Victims by Gender",
                "content": f"Female: {int(total_by_gender.get('Female', 0)):,}<br>Male: {int(total_by_gender.get('Male', 0)):,}",
                "description": "Identified gender",
            },
            {
                "title": "Victims by Age",
                "content": f"Minors: {total_by_age['Minors']:,}<br>Adults: {total_by_age['Adults']:,}",
                "description": "Identified age",
            },
        ]

        # CSS for KPI boxes
        st.markdown(
            """
            <style>
                .kpi-container {
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    height: 180px;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Add subtle gray drop shadow */
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                    background-color: #f9f9f9;
                }
                .kpi-title {
                    color: navy;
                    font-family: 'Sans', sans-serif;
                    font-size: 18px; /* Reduced font size for smaller titles */
                    font-weight: 600;
                }
                .kpi-content {
                    font-size: 20px;
                    font-weight: bold;
                    line-height: 1.5; /* Default size for other KPIs */
                }
                .kpi-content-large {
                    font-size: 28px; /* Larger size for the first KPI value */
                    font-weight: bold;
                    line-height: 1.5;
                }
                .kpi-subtitle {
                    font-size: 14px;
                    color: gray;
                }
                .line-chart-title {
                    font-family: 'Sans', sans-serif;
                    font-size: 28px;
                    font-weight: bold;
                    color: navy;
                    text-align: center;
                    margin-bottom: 20px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Render KPIs
        columns = st.columns(3)
        for i, metric in enumerate(metrics):
            with columns[i]:
                # Use larger font size for the first KPI's value
                content_class = "kpi-content-large" if i == 0 else "kpi-content"
                st.markdown(
                    f"""
                    <div class="kpi-container">
                        <div class="kpi-title">{metric['title']}</div>
                        <div class="{content_class}">{metric['content']}</div>
                        <div class="kpi-subtitle">{metric['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Add vertical space after KPIs
        st.markdown("<br><br>", unsafe_allow_html=True)  
        st.divider()  

        # Use `ui.tabs` for switching between "By Gender" and "By Age Group"
        analysis_type = ui.tabs(
            options=["By Gender", "By Age Group"],
            default_value="By Gender",
            key="analysis_type"
        )

        # Visualization based on selected tab
        if analysis_type == "By Gender":
            # Filter out "Other"
            gender_data = filtered_data[(filtered_data['Sex'].notna()) & (filtered_data['Sex'] != "Other")]
            gender_data = gender_data.groupby(['Year', 'Sex'], as_index=False)['txtVALUE'].sum()
            st.markdown('<div class="line-chart-title">Trafficking Trends by Gender in the U.S.</div>', unsafe_allow_html=True)
            fig = px.line(
                gender_data,
                x="Year",
                y="txtVALUE",
                color="Sex",
                labels={"txtVALUE": "Victims", "Sex": "Gender"},
                color_discrete_map={"Male": "#1f77b4", "Female": "#ff7f0e"},  # Custom colors for Male and Female
            )
        elif analysis_type == "By Age Group":
            age_data = filtered_data[filtered_data['Age'].notna()].groupby(['Year', 'Age'], as_index=False)['txtVALUE'].sum()
            st.markdown('<div class="line-chart-title">Trafficking Trends by Age Group in the U.S.</div>', unsafe_allow_html=True)
            fig = px.line(
                age_data,
                x="Year",
                y="txtVALUE",
                color="Age",
                labels={"txtVALUE": "Victims", "Age": "Age Group"},
                color_discrete_map={"0 to 17 years": "#2ca02c", "18 years or over": "#d62728"},  # Custom colors for Age Groups
            )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Conviction and Prosecution Rates":
    # Header image
    st.image("header3.jpg", use_container_width=True)

    # Page layout with blank margins
    left_margin, content_area, right_margin = st.columns([1, 6, 1])  # 1: Blank margin, 6: Content area, 1: Blank margin

    with content_area:
        # Centered Tabs
        vulnerabilities_tab, traffickers_tab, control_tab, survivors_tab = st.tabs(
            ["Vulnerabilities", "Traffickers", "Control", "Survivors"]
        )

        # Page title under tabs
        st.markdown(
            """
            <style>
                .page-title {
                    font-family: 'Sans', sans-serif;
                    font-size: 28px;
                    font-weight: bold;
                    color: navy;
                    text-align: center;
                    margin-top: 20px;  /* Add spacing above the title */
                }
            </style>
            <div class="page-title">Convictions and Prosecution Rates</div>
            """,
            unsafe_allow_html=True,
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
                <a href="https://polarisproject.org/vulnerabilities-and-recruitment/" target="_blank" class="button-learn-more">Learn More</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 2: Traffickers
    with traffickers_tab:
        st.markdown(
            """
            <style>
                .traffickers-title {
                    font-family: 'Sans', sans-serif;
                    font-size: 18px;
                    font-weight: 600;
                    color: navy;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .traffickers-body {
                    font-family: 'Sans', sans-serif;
                    font-size: 14px;
                    font-weight: 300;
                    color: black;
                    text-align: center;
                }
            </style>
            <div class="traffickers-title">Traffickers</div>
            <div class="traffickers-body">
                Content for Traffickers goes here.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 3: Control
    with control_tab:
        st.markdown(
            """
            <style>
                .control-title {
                    font-family: 'Sans', sans-serif;
                    font-size: 18px;
                    font-weight: 600;
                    color: navy;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .control-body {
                    font-family: 'Sans', sans-serif;
                    font-size: 14px;
                    font-weight: 300;
                    color: black;
                    text-align: center;
                }
            </style>
            <div class="control-title">Control</div>
            <div class="control-body">
                Content for Control goes here.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 4: Survivors
    with survivors_tab:
        st.markdown(
            """
            <style>
                .survivors-title {
                    font-family: 'Sans', sans-serif;
                    font-size: 18px;
                    font-weight: 600;
                    color: navy;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .survivors-body {
                    font-family: 'Sans', sans-serif;
                    font-size: 14px;
                    font-weight: 300;
                    color: black;
                    text-align: center;
                }
            </style>
            <div class="survivors-title">Survivors</div>
            <div class="survivors-body">
                Content for Survivors goes here.
            </div>
            """,
            unsafe_allow_html=True
        )
