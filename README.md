# Human Trafficking Trends Analysis App

## Streamlit Cloud Link
App: https://humantrafficking.streamlit.app

## Introduction
This project presents a comprehensive streamlit app dashboard analyzing human trafficking trends globally and regionally, with a specific focus on the United States. The app leverages UNODC trafficking data to visualize key metrics, including victim demographics by gender and age, as well as prosecution and conviction rates. The primary objective is to provide insights into global and U.S. trafficking patterns, demographic distributions, and legal response effectiveness. By integrating interactive visuals, this project enables users to explore trafficking data across multiple dimensions, supporting a deeper understanding of regional and temporal trends in trafficking cases.

## Data/Operation Abstraction Design

### Key Visualizations
**Global and Regional Trends** A map with gradient colors to represent the intensity of trafficking incidents by country. This layered approach allows users to quickly identify high-incidence areas both visually and quantitatively.

**Gender and Age Distributions** 3 dynamnic KPIs for Total detected victims, detected victims identified by gender, and detected victims identified by age in the US by year. A multi line graph offer insights into gender and age demographics of trafficking victims over a year range, using the toggle and slider, providing an interactive exploration of vulnerable populations over time.

**Prosecution and Conviction Rates** A combined bar chart and line graph show convicted versus prosecuted cases over time. The bar chart represents prosecutions, while the line overlays convictions, along with a dynamic KPI for the average conviction rate over the given year range, allowing for an intuitive comparison of legal outcomes and the progression from prosecution to conviction.

These visualizations collectively provide a clear abstraction of the trafficking process, from detection to legal outcomes. Calculated fields, such as conviction rates and demographic totals, ensure consistent aggregation across years, countries, and categories, while interactive filters and calculated fields support dynamic comparisons across multiple dimensions.

## Future Enhancements:
Advanced Filtering Options: Incorporating multi-level drill-down capabilities for specific states or local regions within the U.S. would allow for more detailed geographic insights.
Predictive Analytics: Introducing trend forecasting for prosecution and conviction rates could help anticipate future changes and identify emerging trends in trafficking cases.

## Data UNODC - Metadata Information
**Trafficking in Persons**
The tables include figures on detected trafficking victims and persons convicted of
trafficking in persons at national, regional and global level. National data are
submitted by Member States to UNODC through the United Nations Questionnaire
for the Global Report on Trafficking in Persons (GLOTIP) or other means.
Dataset characteristics

**Access Link** https://dataunodc.un.org/dp-trafficking-persons

**Original DataSet**https://dataunodc.un.org/sites/dataunodc.un.org/files/data_glotip.xlsx

**MetaData**https://dataunodc.un.org/sites/dataunodc.un.org/files/metadata_trafficking_in_persons.pdf

**Last Update:** 24/01/2023

**Base Period:** Calendar Year

**Data Source(s):**  National data on trafficking in persons collected through the GLOTIP. Please see below for National data collection sources:

<u>Contact</u>
United Nations Office on Drugs and Crime
Email: unodc-ddds@un.org 
