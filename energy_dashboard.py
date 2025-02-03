#Energy Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
 
# ------------------ Custom Styling -------------------
 
st.set_page_config(
    page_title="Energy Dashboard",
    layout="wide",
    initial_sidebar_state="auto"
)
 
# **Prepared By Information Box at the Bottom**
st.sidebar.markdown(
    """
    <div style="background-color: transparent; border-radius: 5px; margin-top: 20px;">
        <p style="font-size: 14px; font-weight: bold; color: #a9a9a9; text-align: left;">
            Dashboard by: Puvana Venkidasalam
        </p>
    </div>
    """, unsafe_allow_html=True
)
 
# ------------------ Load Dataset ------------------
file_path = r"C:\Users\puvanavks\OneDrive\Desktop\Energy Dashboard\Processed_Merged_Energy_Data.xlsx"

# Check if the file exists
if not os.path.exists(file_path):
    st.error("File not found at the given path")
    st.stop()  # Stop execution immediately

# Try loading the dataset
try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()  # Stop execution immediately


# ------------------ Sidebar Filters ------------------
st.sidebar.markdown(
    """
    <div style="background-color: #D3D3D3; padding: 5px; border-radius: 5px; margin-bottom: 20px;">
        <h3 style="font-weight: bold; font-size: 18px; color: black; text-align: left; padding-left: 10px;">
            Filters
        </h3>
    </div>
    """, unsafe_allow_html=True
)
 
# **Static Region Selector with Checkboxes**
selected_regions = []
 
# Custom styled header for "Select Region(s)"
st.sidebar.markdown(
    """
    <h3 style="font-size: 16px; font-weight: bold; margin-bottom: 10px; text-align: left; padding-left: 10px;">
        Select Region(s):
    </h3>
    """, unsafe_allow_html=True
)
 
# Ensure the 'Region' column exists in the DataFrame
if 'Region' in df.columns:
    # Get all unique regions in the dataset
    all_regions = sorted(df['Region'].unique())  # Remove duplicates and sort
 
    # Create checkboxes for each region
    for region in all_regions:
        if st.sidebar.checkbox(region, value=True, key=f"region_checkbox_{region}"):
            selected_regions.append(region)
else:
    st.sidebar.warning("The 'Region' column does not exist in the dataset.")
 
# Custom styled header for "Select Year Range"
st.sidebar.markdown(
    """
    <h3 style="font-size: 16px; font-weight: bold; margin-top: 20px; text-align: left; padding-left: 10px;">
        Select Year Range:
    </h3>
    """, unsafe_allow_html=True
)
 
# ------------------ Year Range Slider ------------------
year_range = st.sidebar.slider(
    "",
    min_value=2000,  # Set min value to 2000
    max_value=2023,  # Set max value to 2023
    value=(2000, 2023)  # Adjust default value to start from 2000
)
 
# ------------------ Data Filtering ------------------
# Ensure that the DataFrame is not empty before filtering
if 'df' in locals() and not df.empty:
    filtered_data = df[df["Region"].isin(selected_regions)]
 
    # Apply year filters
    final_data = filtered_data[
        (filtered_data["Year"] >= year_range[0]) &
        (filtered_data["Year"] <= year_range[1])
    ].copy()
 
    # Display a warning if no data matches the filters
    if final_data.empty:
        st.sidebar.warning("No data available for the selected filters. Please adjust your selections.")
else:
    st.sidebar.error("The dataset is empty or not loaded properly.")
 
st.markdown(
    """
    <h1 style="text-align: center;
              padding: 20px;
              background-color: #4CAF50;
              color: white;
              border-radius: 10px;
              border: 5px solid white;"> <!-- White border -->
        Energy Consumption Dashboard
    </h1>
    <h3 style="text-align: center; color: grey; font-size: 36px; font-weight: bold;">2000-2023</h3> <!-- Bigger font size for 2000-2023 -->
    <p style="text-align: center; color: grey; font-size: 16px; padding: 15px; width: 90%; margin: auto; font-weight: bold;">
        This dashboard provides essential insights into primary <span style="color: #FFD700;">energy consumption</span> patterns and their connection to regional economic factors, population, and energy sources.
        Analyzing historical trends, such as global primary <span style="color: #FFD700;">energy consumption</span> by region and the proportion of <span style="color: #FFD700;">energy sources</span>, helps identify areas of high demand and the shift towards <span style="color: #FFD700;">renewable energy</span>.
        The <span style="color: #FFD700;">economic impact</span> analyses, like <span style="color: #FFD700;">energy consumption</span> vs. GDP and population, offer valuable context for understanding the drivers of primary energy use.
        Additionally, energy consumption forecasts are vital for future planning, helping policymakers and businesses make informed decisions on resource allocation, infrastructure development,
        and strategies for <span style="color: #FFD700;">sustainability</span>.
    </p>
    """, unsafe_allow_html=True
)


 
# Divider between sections
st.markdown("---")
 
# ------------------ Overview Section ---------------------
st.markdown(
    """
    <h2 style="color: #FF7F32; text-align: center;">Energy Consumption Historical Trends</h2>
    """, unsafe_allow_html=True
)

st.write("""
    <div style="text-align: center; width: 80%; margin: auto;">
        This section provides a high-level summary of the key insights from the entire dashboard,
        including global trends, regional variations, and major contributors to energy consumption.
    </div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <p style="text-align: center; color: grey; font-size: 16px; padding: 0; width: 80%; margin: auto;">
        Hover over charts to get options to Download Plot as a PNG, Zoom, Pen, Zoom In, Zoom Out, Auto Scale, Reset Axis, Full Screen.
        <br><br>
    </p>
    """, unsafe_allow_html=True
)

if not final_data.empty:
    # Create columns for side-by-side charts with dividers
    col1, col_divider1, col2, col_divider2, col3 = st.columns([4, 0.1, 4, 0.1, 4])

    # Global Trends per Region
    with col1:
        trend_data = final_data.groupby(["Year", "Region"]).agg({
            "primary_energy_consumption": "sum",
            "gdp": "mean",
            "population": "mean"
        }).reset_index()

        fig_trends = px.line(
            trend_data,
            x="Year",
            y="primary_energy_consumption",
            color="Region",  # Color the lines by Region
            title="Global Energy Consumption Trends by Region",
            labels={"primary_energy_consumption": "Energy Consumption (TWH)", "Year": "Year"},
            markers=True
        )
        fig_trends.update_layout(
            height=400,  # Fixed height for consistency
            margin={"t": 40, "b": 80, "l": 50, "r": 50}  # Ensure consistent margins
        )
        st.plotly_chart(fig_trends, use_container_width=True)

    # Vertical light grey divider between Global Trends and Energy Source Contribution
    with col_divider1:
        st.markdown(
            """
            <div style="width: 2px; height: 400px; background-color: #D3D3D3; margin: auto;"></div>
            """,
            unsafe_allow_html=True
        )

    # Energy Source Contribution per Region
    with col2:
        energy_sources = final_data.groupby("Region")[["oilcons_ej", "coalcons_ej", "gascons_ej", "ren_power_ej"]].sum().reset_index()

        # Calculate the sum of each energy source column across regions
        energy_sources_sum = energy_sources[["oilcons_ej", "coalcons_ej", "gascons_ej", "ren_power_ej"]].sum()

        # Create a pie chart using the total sums for each energy source
        energy_pie = px.pie(
            names=energy_sources_sum.index,  # Names are the energy sources (columns)
            values=energy_sources_sum.values,  # Values are the summed consumption for each source
            title="Proportion of Energy Sources by Region",
            hole=0.4
        )
        energy_pie.update_layout(
            height=400,  # Fixed height for consistency
            margin={"t": 40, "b": 80, "l": 50, "r": 50}  # Ensure consistent margins
        )
        st.plotly_chart(energy_pie, use_container_width=True)

    # Vertical light grey divider between Energy Source Contribution and Top Countries
    with col_divider2:
        st.markdown(
            """
            <div style="width: 2px; height: 400px; background-color: #D3D3D3; margin: auto;"></div>
            """,
            unsafe_allow_html=True
        )

    # Top Energy Consuming Countries by Region
    with col3:
        top_countries = final_data.groupby(["Region", "Country"])["primary_energy_consumption"].sum().reset_index()
        top_countries_region = top_countries[top_countries["Region"].isin(selected_regions)]

        # Sort the data before applying nlargest to ensure proper alignment
        top_countries_region_sorted = top_countries_region.sort_values("primary_energy_consumption", ascending=False)
        top_countries_region_sorted = top_countries_region_sorted.groupby("Region").head(3).reset_index(drop=True)

        fig_top_countries = px.bar(
            top_countries_region_sorted,
            x="primary_energy_consumption",
            y="Country",
            color="Region",
            orientation="h",
            title="Top 3 Energy Consuming Countries by Region",
            labels={"primary_energy_consumption": "Energy Consumption (TWH)", "Country": "Country"}
        )
        
        fig_top_countries.update_layout(
            height=400,  # Fixed height for consistency
            margin={"t": 40, "b": 80, "l": 50, "r": 50},  # Ensure consistent margins
            yaxis=dict(tickmode='linear', tickangle=0),  # Ensure y-axis labels are not skipped
        )

        st.plotly_chart(fig_top_countries, use_container_width=True)

else:
    st.write("No data to display for the selected filters.")

# Divider between sections
st.markdown("---")

 
# ------------------ Economic Impact Section ----------------------
st.markdown(
    """
    <h2 style="color: #FF7F32; text-align: center;">Economic Impact on Regional Energy Consumption </h2>
    """, unsafe_allow_html=True
)
 
 
st.write("""
    <div style="text-align: center; width: 80%; margin: auto;">
        This section aims to explore the relationship between economic and demographic factors and their impact on energy consumption across different regions.
        It is valuable in analysing how GDP and population correlate with energy usage to identify trends and patterns that can inform sustainable energy planning and policy-making.
    </div>
""", unsafe_allow_html=True)
 
st.markdown(
    """
    <p style="text-align: center; color: grey; font-size: 16px; padding: 0; width: 80%; margin: auto;">
        Hover over charts to get options to Download Plot as a PNG, Zoom, Pen, Zoom In, Zoom Out, Auto Scale, Reset Axis, Full Screen.
        <br><br>  <!-- Add line breaks for spacing -->
    </p>
    """, unsafe_allow_html=True
)

 
# Extract the final year from the selected year range
final_year = year_range[1]  # Get the maximum (final) year from the slider
 
if not final_data.empty:
    # Filter data based on the final year and regions
    selected_regions = final_data["Region"].unique()  # Get unique regions
    filtered_data = final_data[
        (final_data["Year"] == final_year) & (final_data["Region"].isin(selected_regions))
    ]
 
    if not filtered_data.empty:
        # Group the data by region and aggregate the relevant columns
        grouped_data = filtered_data.groupby("Region").agg(
            total_gdp=('gdp', 'sum'),
            total_population=('population', 'sum'),
            total_energy_consumption=('primary_energy_consumption', 'sum'),
            number_of_countries=('Country', 'nunique')  # Count unique countries in each region
        ).reset_index()
 
# Create columns for side-by-side charts
col1, col_divider, col2 = st.columns([4, 0.1, 4])  # Adjust column width proportions as needed
 
# Energy Consumption vs. GDP (1 bubble for each region)
with col1:
    fig1 = px.scatter(
        grouped_data,
        x="total_gdp",
        y="total_energy_consumption",
        color="Region",  # Color by Region
        size="number_of_countries",  # Bubble size by number of countries
        title=f"Energy Consumption vs. GDP by Region (Year {final_year})",
        size_max=50  # Adjust size scale for better visualization
    )
    st.plotly_chart(fig1)
 
# Vertical grey divider with fixed height
with col_divider:
    st.markdown(
        """
        <div style="width: 2px; height: 400px; background-color: #D3D3D3; margin: auto;"></div>
        """,
        unsafe_allow_html=True
    )
 
# Energy Consumption vs. Population (1 bubble for each region)
with col2:
    fig2 = px.scatter(
        grouped_data,
        x="total_population",
        y="total_energy_consumption",
        color="Region",  # Color by Region
        size="number_of_countries",  # Bubble size by number of countries
        title=f"Energy Consumption vs. Population by Region (Year {final_year})",
        size_max=50  # Adjust size scale for better visualization
    )
    st.plotly_chart(fig2)
 
# Add note below the charts
st.markdown(
    """
    <p style="text-align: center; color: grey; font-size: 14px;">
        <i><b>Note:</b> The bubble size represents the number of countries within the region.</i>
    </p>
    """,
    unsafe_allow_html=True
)
 
# Divider between sections
st.markdown("---")
 
# ------------------ Predictive Modeling Section -------------------------
 
st.markdown(
    """
<h2 style="color: #FF7F32; text-align: center;">Energy Consumption Forecast in TWH</h2>
    """, unsafe_allow_html=True
)
 
 
st.write("""
    <div style="text-align: center; width: 80%; margin: auto;">
        This section uses ARIMA (AutoRegressive Integrated Moving Average) to forecast energy consumption trends.
        By analyzing historical data, it provides actionable insights to support decision-making, optimize resources,
        and plan for future energy needs effectively.
    </div>
""", unsafe_allow_html=True)
 
st.markdown(
    """
    <p style="text-align: center; color: grey; font-size: 16px; padding: 0; width: 80%; margin: auto;">
        Hover over charts to get options to Download Plot as a PNG, Zoom, Pen, Zoom In, Zoom Out, Auto Scale, Reset Axis, Full Screen.
    </p>
    <br> <!-- This adds one line break -->
    """, unsafe_allow_html=True
)
 
# Create two columns: one for the filters and one for the chart
col1, col2 = st.columns([1, 2])  # Define layout with desired width ratio
 
# Exclude specific countries from the dropdown options
excluded_countries = ["Chad", "Curacao", "Guyana",
                      "Mozambique", "Papua New Guinea",
                      "Serbia", "South Sudan"]
 
available_countries = final_data[~final_data["Country"].isin(excluded_countries)]["Country"].unique()
 
with col1:
    # Dropdown to select countries for prediction (allow selecting multiple countries)
    selected_countries_predict = st.multiselect(
        "Select Countries for Prediction (Up to 2):",
        options=available_countries,  # Use the filtered country list
        default=[available_countries[0]],  # Dynamically set the default to the first country in the list
        max_selections=2  # Limit to two countries
    )
 
    # Input fields for projected growth rates
 
    # GDP Growth slider with range from -5% to 10% and default value set to 0
    gdp_growth = st.slider(
        "Projected Gross Domestic Product (GDP) Growth (%)",
        min_value=-5.0,
        max_value=10.0,  # Adjusted maximum value for GDP growth
        value=0.0,  # Default value set to 0
        step=0.1
    )
 
    # Population Growth slider with range from -2% to 5% and default value set to 0
    population_growth = st.slider(
        "Projected Population Growth (%)",
        min_value=-2.0,
        max_value=5.0,  # Adjusted maximum value for population growth
        value=0.0,  # Default value set to 0
        step=0.1
    )
 
with col2:
    st.subheader(f"Predictive Analysis for {', '.join(selected_countries_predict)}")
 
    # Add statement below the title of the prediction chart with a darker gray background
   
    st.markdown(
        """
        <div style="background-color: #d9d9d9;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                    color: black;
                    margin-top: -10px;">
            <strong>Analyse by:</strong><br>
            - <strong>Simulating Economic Scenarios:</strong> Adjust GDP and population growth rates to model future energy consumption trends and explore localized scenarios for more accurate forecasts.<br>
            - <strong>Comparing Countries:</strong> Select and overlay the energy consumption trends of two countries to directly compare their patterns and identify regional differences.
        </div>
        """, unsafe_allow_html=True
    )
 
 
    # Filter data for the selected countries
    countries_data = final_data[final_data["Country"].isin(selected_countries_predict)]
 
    if not countries_data.empty:
        # Prepare time series data for ARIMA
        ts_data = countries_data.groupby(["Year", "Country"])["primary_energy_consumption"].sum().unstack(fill_value=0)
 
        # Prepare the forecast for each selected country
        forecast_combined = []
 
        for country in selected_countries_predict:
            # Fit the ARIMA model with data up to 2023
            model = ARIMA(ts_data[country].loc[ts_data.index <= 2023], order=(2, 1, 2))  # Example ARIMA parameters (p=2, d=1, q=2)
            model_fit = model.fit()
 
            # Forecast for the prediction period (2024-2028)
            future_years = np.arange(2024, 2029)
            future_forecast = model_fit.forecast(steps=len(future_years))
 
            # Adjust for GDP and population growth
            adjusted_forecast = (
                future_forecast * (1 + (gdp_growth / 100)) * (1 + (population_growth / 100))
            )
 
            # Prepare future forecast DataFrame
            future_forecast_df = pd.DataFrame({
                "Year": future_years,
                f"Predicted Energy Consumption (TWH) - {country}": adjusted_forecast
            })
 
            forecast_combined.append(future_forecast_df.set_index("Year")[f"Predicted Energy Consumption (TWH) - {country}"])
 
        # Combine historical and forecast data for plotting
        historical_data_combined = ts_data.loc[ts_data.index <= 2023]
        forecast_combined_df = pd.concat(forecast_combined, axis=1)
 
        # Create a DataFrame for combined data for plotting
        combined_data = pd.concat([historical_data_combined, forecast_combined_df], axis=1).reset_index()
 
        # Generate the forecast plot
        fig_forecast = px.line(
            combined_data,
            x="Year",
            y=combined_data.columns[1:],  # All forecast columns
            title=f"Energy Consumption Forecast for {', '.join(selected_countries_predict)}",
            labels={"Year": "Year", "Energy Consumption (TWH)": "Energy Consumption (TWH)"},
            markers=True
        )
 
        # Highlight predicted values with a different color
        for trace in fig_forecast.data:
            if 'Predicted' in trace.name:
                trace.line.color = 'orange'  # Set color for predicted data
 
        # Add a vertical dotted line at 2023
        fig_forecast.add_vline(
            x=2023,
            line_dash="dot",
            line_color="red",
            annotation_text="Forecast Start",
            annotation_position="top"
        )
 
        # Display the plot
        st.plotly_chart(fig_forecast, use_container_width=True)
 
    else:
        st.warning(f"No data available for {', '.join(selected_countries_predict)}.")
 
 
# Divider between sections
st.markdown("---")
 
# Add data sources section aligned to the right and styled in green
 
st.markdown(
    """
    <div style="text-align: center; color: white; font-size: 16px; margin-top: 10px; background-color: #808080; border-radius: 5px; font-weight: normal; border: 2px solid black;">
        <strong style="font-size: 18px; color: white;">Data Source:</strong><br>
        Energy Institute (Up to 2023)<br>
        OurWorldInData.org (Up to 2023)
    </div>
    """, unsafe_allow_html=True
)
 
 
# Divider between sections
st.markdown("---")
 
