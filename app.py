import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui
from PIL import Image
import os
import base64
import plotly.graph_objects as go

# Set up page configuration
st.set_page_config(page_title="Trafficking Dashboard", page_icon="images/icon.png", layout="wide")

def display_header_image(image_filename):
    """
    Displays a header image as a responsive full-width image.

    Args:
        image_filename (str): The relative path to the image file.
    """
    # Get the full path to the image
    image_path = os.path.join(os.path.dirname(__file__), image_filename)

    # Check if the image file exists
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        st.markdown(
            f"""
            <style>
            .full-width-image {{
                width: 100%;
                height: auto;
            }}
            </style>
            <img class="full-width-image" src="data:image/jpg;base64,{encoded_string}">
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error(f"Image file not found: {image_filename}")

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
image = Image.open("images/icon.png")
resized_image = image.resize((632, 118))
st.sidebar.image(resized_image)

# Sidebar radio buttons
selected_tab = st.sidebar.radio(
    "",
    options=["Overview", "Trafficking Over Time", "Conviction and Prosecution Rates"],
)

# Initialize session state for inputs
if "date_range" not in st.session_state:
    st.session_state["date_range"] = None
if "selected_countries" not in st.session_state:
    st.session_state["selected_countries"] = ["All Countries"]
if "selected_years" not in st.session_state:
    st.session_state["selected_years"] = (2007, 2020)
if "analysis_type" not in st.session_state:
    st.session_state["analysis_type"] = "By Gender"

@st.cache_data
def load_data(file_path, sheet_name="data_glotip_1"):
    """
    Loads data from an Excel file with caching for improved performance.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): The sheet name to load data from. Defaults to "data_glotip_1".

    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    # Load the data
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Ensure txtVALUE is numeric and replace "<5" with 2
    data['txtVALUE'] = pd.to_numeric(data['txtVALUE'], errors='coerce')
    data.loc[data['txtVALUE'] < 5, 'txtVALUE'] = 2

    return data

# Load the data using the cached function
file_path = "data/data_glotip.xlsx"
data = load_data(file_path)

# Ensure txtVALUE is numeric and replace "<5" with 2
data['txtVALUE'] = pd.to_numeric(data['txtVALUE'], errors='coerce')
data.loc[data['txtVALUE'] < 5, 'txtVALUE'] = 2

# Content rendering based on selected tab
if selected_tab == "Overview":
    # Header image
    display_header_image("images/header.jpg")

    # Row 1: Description columns
    col1, col2 = st.columns(2)
    min_year, max_year = int(data["Year"].min()), int(data["Year"].max())

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
            value=st.session_state["date_range"] or (min_year, max_year),
            step=1
        )
        st.session_state["date_range"] = date_range


        # Country dropdown
        country_list = ["All Countries"] + sorted(data["Country"].dropna().unique())
        selected_countries = st.multiselect(
            "Select Country/Countries",
            options=country_list,
            default=st.session_state["selected_countries"]
        )
        st.session_state["selected_countries"] = selected_countries


        # Filter data by date range and selected countries
        overview_data = data[
            (data["Year"] >= date_range[0]) & (data["Year"] <= date_range[1])
        ]
        if "All Countries" not in selected_countries:
            overview_data = overview_data[overview_data["Country"].isin(selected_countries)]

    with map_col:
        # Prepare filtered data for the map
        map_data = overview_data.groupby("Country", as_index=False)["txtVALUE"].sum()
        fig = px.choropleth(
            map_data,
            locations="Country",
            locationmode="country names",
            color="txtVALUE",
            color_continuous_scale="oranges",
            labels={"txtVALUE": "Victims"}
        )
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type="equirectangular")
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Trafficking Over Time":
    # Header image
    display_header_image("images/header2.jpg")

    # Filter data
    data["Country"] = data["Country"].str.strip().str.title()
    us_data = data[(data["Country"] == "United States Of America") & (data["Year"] >= 2007) & (data["Year"] <= 2020) ]

    if us_data.empty:
        st.warning("No data available.")
    else:
        # Clean the Year column
        us_data = us_data.dropna(subset=["Year"]) 
        us_data["Year"] = pd.to_numeric(us_data["Year"], errors="coerce")
        us_data = us_data.dropna(subset=["Year"])

        # Year slider
        if us_data.empty:
            st.warning("No data available for the selected criteria.")
            min_year, max_year = 2000, 2020  # Replace with appropriate defaults
        else:
            min_year, max_year = int(us_data["Year"].min()), int(us_data["Year"].max())

        if "trafficking_years" not in st.session_state:
            st.session_state["trafficking_years"] = (min_year, max_year)

        selected_years = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=st.session_state["trafficking_years"],
            key="trafficking_year_slider"
        )
        st.session_state["trafficking_years"] = selected_years



        # Filter data by selected years
        line_filtered_data = us_data[
            (us_data["Year"] >= selected_years[0]) & (us_data["Year"] <= selected_years[1])
        ]

        # Replace "Total" with "All victims" in the relevant columns
        line_filtered_data["Sex"] = line_filtered_data["Sex"].replace("Total", "All victims")
        line_filtered_data["Age"] = line_filtered_data["Age"].replace("Total", "All victims")

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
        total_victims = int(line_filtered_data['txtVALUE'].sum())
        total_by_gender = line_filtered_data.groupby('Sex')['txtVALUE'].sum()
        total_by_gender = total_by_gender[["Female", "Male"]] if "Female" in total_by_gender and "Male" in total_by_gender else total_by_gender
        total_by_age = line_filtered_data.groupby('Age')['txtVALUE'].sum()
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

        # Use ui.tabs for switching between "By Gender" and "By Age Group"
        line_line_filtered_data = us_data[
            (us_data["Year"] >= selected_years[0]) & (us_data["Year"] <= selected_years[1])
        ]

       # Line charts for gender and age group
        analysis_type = ui.tabs(
            options=["By Gender", "By Age Group"],
            default_value=st.session_state["analysis_type"]
        )
        st.session_state["analysis_type"] = analysis_type

        if analysis_type == "By Gender":
            gender_data = line_filtered_data[
                ~line_filtered_data["Sex"].isin(["Other", "Unknown"])
            ].groupby(["Year", "Sex"], as_index=False)["txtVALUE"].sum()

            # Define the color mapping to ensure "All victims" is red
            color_map = {
                "All victims": "red",
                "Female": "orange",
                "Male": "blue"
            }

            fig = px.line(
                gender_data,
                x="Year",
                y="txtVALUE",
                color="Sex",
                labels={"txtVALUE": "Victims", "Sex": "Gender"},
                title="Trafficking Trends by Gender",
                color_discrete_map=color_map
            )

        elif analysis_type == "By Age Group":
            age_data = line_filtered_data[
                ~line_filtered_data["Age"].isin(["Other", "Unknown"])
            ].groupby(["Year", "Age"], as_index=False)["txtVALUE"].sum()

            # Define the color mapping to ensure "All victims" is red
            color_map = {
                "All victims": "red",
                "0 to 17 years": "orange",
                "18 years or over": "blue"
            }

            fig = px.line(
                age_data,
                x="Year",
                y="txtVALUE",
                color="Age",
                labels={"txtVALUE": "Victims", "Age": "Age Group"},
                title="Trafficking Trends by Age Group",
                color_discrete_map=color_map
            )


        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Conviction and Prosecution Rates":
    # Header image
    display_header_image("images/header3.jpg")


    # Page layout: # 1: Blank margin, 6: Content area, 1: Blank margin
    left_margin, content_area, right_margin = st.columns([1, 6, 1])

    with content_area:
        # Centered Tabs
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
                    <a href="https://polarisproject.org/vulnerabilities-and-recruitment/" target="_blank" class="button-learn-more">Learn More</a>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Tab 2: Traffickers
        with traffickers_tab:
            st.markdown(
                """
                <div class="traffickers-title" style="font-family: 'Sans', sans-serif; font-size: 18px; font-weight: 600; color: navy; text-align: center; margin-bottom: 20px;">Who are the traffickers?</div>
                <div class="traffickers-body" style="font-family: 'Sans', sans-serif; font-size: 14px; font-weight: 300; color: black; text-align: center;">
                    Perpetrators of human trafficking span all racial, ethnic, and gender demographics and are as diverse as survivors. 
                    Some use their privilege, wealth, and power as a means of control while others experience the same socio-economic 
                    oppression as their victims. They include individuals, business owners, members of a gang or network, parents or 
                    family members of victims, intimate partners, owners of farms or restaurants, and powerful corporate executives 
                    and government representatives.
                </div>
                """,
                unsafe_allow_html=True
            )

        # Tab 3: Control
        with control_tab:
            st.markdown(
                """
                <div class="control-title" style="font-family: 'Sans', sans-serif; font-size: 18px; font-weight: 600; color: navy; text-align: center; margin-bottom: 20px;">How do traffickers control victims?</div>
                <div class="control-body" style="font-family: 'Sans', sans-serif; font-size: 14px; font-weight: 300; color: black; text-align: center; margin-bottom: 20px;">
                    Traffickers employ a variety of control tactics, the most common include physical and emotional abuse and threats, 
                    isolation from friends and family, and economic abuse. They make promises aimed at addressing the needs of their 
                    target in order to impose control. As a result, victims become trapped and fear leaving for myriad reasons, 
                    including psychological trauma, shame, emotional attachment, or physical threats to themselves or their family.
                </div>
                <div style="text-align: center;">
                    <a href="https://polarisproject.org/understanding-human-trafficking/" target="_blank" class="button-learn-more">Learn More</a>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Tab 4: Survivors
        with survivors_tab:
            st.markdown(
                """
                <div class="survivors-title" style="font-family: 'Sans', sans-serif; font-size: 18px; font-weight: 600; color: navy; text-align: center; margin-bottom: 20px;">Who are the survivors?</div>
                <div class="survivors-body" style="font-family: 'Sans', sans-serif; font-size: 14px; font-weight: 300; color: black; text-align: center; margin-bottom: 20px;">
                    Victims and survivors of human trafficking represent every race and ethnicity but some forms of trafficking 
                    are more likely to affect specific ethnic groups.
                </div>
                <div style="text-align: center;">
                    <a href="https://polarisproject.org/our-approach/" target="_blank" class="button-learn-more">Learn More</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        # Add vertical space after KPIs 
        st.divider()  

    # Step 1: Replace '<5' with 2 in txtVALUE
    data['txtVALUE'] = pd.to_numeric(data['txtVALUE'], errors='coerce')
    data.loc[data['txtVALUE'] < 5, 'txtVALUE'] = 2

    # Step 2: Filter for the United States
    data["Country"] = data["Country"].str.strip().str.title()
    us_data = data[data["Country"] == "United States Of America"]

    # Step 3: Filter for relevant indicators
    us_data = us_data[us_data["Indicator"].isin(["Persons prosecuted", "Persons convicted"])]

    # Step 4: Filter for Dimension = "Total"
    us_data = us_data[us_data["Dimension"] == "Total"]

    # Step 5: Filter for Year range (2007–2020)
    us_data = us_data[(us_data["Year"] >= 2007) & (us_data["Year"] <= 2020)]

    # Check if the filtered dataset is empty
    if us_data.empty:
        st.warning("No data available for the United States of America from 2007 to 2020 in the selected dataset.")
    else:
        # Step 6: Aggregate prosecution and conviction data
        prosecution_data = (
            us_data[us_data["Indicator"] == "Persons prosecuted"]
            .groupby("Year", as_index=False)["txtVALUE"]
            .sum()
            .rename(columns={"txtVALUE": "Prosecutions"})
        )
        conviction_data = (
            us_data[us_data["Indicator"] == "Persons convicted"]
            .groupby("Year", as_index=False)["txtVALUE"]
            .sum()
            .rename(columns={"txtVALUE": "Convictions"})
        )

        # Step 7: Merge prosecution and conviction data
        combined_data = pd.merge(prosecution_data, conviction_data, on="Year", how="outer").fillna(0)
        combined_data["Conviction Rate (%)"] = (
            (combined_data["Convictions"] / combined_data["Prosecutions"]) * 100
        ).fillna(0)
        combined_data["Difference"] = combined_data["Prosecutions"] - combined_data["Convictions"]

        # Year slider with session state
        if combined_data.empty:
            st.warning("No data available for the selected criteria.")
            min_year, max_year = 2000, 2020  # Replace with appropriate defaults
        else:
            min_year, max_year = int(combined_data["Year"].min()), int(combined_data["Year"].max())

        if "conviction_years" not in st.session_state:
            st.session_state["conviction_years"] = (min_year, max_year)

        selected_years = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=st.session_state["conviction_years"],
            key="conviction_year_slider"
        )
        st.session_state["conviction_years"] = selected_years


        # Filter data by selected years
        filtered_data = combined_data[
            (combined_data["Year"] >= selected_years[0]) & (combined_data["Year"] <= selected_years[1])
        ]

        # Dynamic page title
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
            <div class="page-title">Convictions and Prosecution Rates ({selected_years[0]} - {selected_years[1]})</div>
            """,
            unsafe_allow_html=True,
        )

        # KPI for average conviction rate
        avg_conviction_rate = filtered_data["Conviction Rate (%)"].mean()
        st.markdown(
            f"""
            <div style="text-align: center; background-color: #f9f9f9; padding: 10px; 
                        border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: navy;">Average Conviction Rate</h4>
                <p style="font-size: 24px; color: black; font-weight: bold;">{avg_conviction_rate:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Create the figure
        fig = go.Figure()

        # Add Prosecutions as a bar chart
        fig.add_trace(
            go.Bar(
                x=filtered_data["Year"],
                y=filtered_data["Prosecutions"],
                name="Prosecutions",  # Explicitly set the name for the legend
                marker_color="#1f77b4",  # Match the color
            )
        )

        # Add Convictions as a line chart
        fig.add_trace(
            go.Scatter(
                x=filtered_data["Year"],
                y=filtered_data["Convictions"],
                mode="lines+markers",
                name="Convictions",  # Explicitly set the name for the legend
                line=dict(color="#ff7f0e", width=2),
            )
        )

        # Add annotations for the difference, Green for positive, Red for negative
        for i in range(len(filtered_data)):
            difference = filtered_data.iloc[i]["Difference"]
            color = "green" if difference > 0 else "red"
            fig.add_annotation(
                x=filtered_data.iloc[i]["Year"],
                y=filtered_data.iloc[i]["Prosecutions"] + 20,
                text=f"{difference:+}",
                showarrow=False,
                font=dict(color=color, size=14, family="Arial Black"),
            )

        # Update layout
        fig.update_layout(
            title=None,
            yaxis=dict(title="Number of People"),
            xaxis=dict(title="Year"),
            showlegend=True,  # Ensure the legend is displayed
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
            barmode="group",  # Group bar and line charts together
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
