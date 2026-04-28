import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page config
st.set_page_config(page_title="Climate Data Dashboard", layout="wide")

# Title and Description
st.title("🌍 Horn of Africa & East Africa Climate Vulnerability Dashboard")
st.markdown("This interactive dashboard visualizes climate metrics across five countries: Ethiopia, Kenya, Nigeria, Sudan, and Tanzania.")

# Cache the data loading function so it only runs once
@st.cache_data
def load_data():
    countries = ['ethiopia', 'kenya', 'nigeria', 'sudan', 'tanzania']
    dfs = []
    
    # We use a relative path assuming the app is run from the project root
    # or deployed with the data folder present.
    # Note: Streamlit Cloud needs the data folder in the repo to fetch it.
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    for c in countries:
        file_path = os.path.join(data_dir, f"{c}_clean.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            dfs.append(df)
        else:
            st.warning(f"Data file for {c} not found at {file_path}")
            
    if dfs:
        data = pd.concat(dfs, ignore_index=True)
        data['date'] = pd.to_datetime(data['date'])
        return data
    else:
        return pd.DataFrame()

# Load Data
data = load_data()

if data.empty:
    st.error("No data available to display. Please ensure the cleaned CSV files are in the 'data' directory.")
    st.stop()

# ----------------- Sidebar Controls -----------------
st.sidebar.header("Dashboard Controls")

# 1. Country Selector (Multi-select)
available_countries = data['Country'].unique().tolist()
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare:",
    options=available_countries,
    default=available_countries
)

# 2. Year Range Slider
min_year = int(data['Year'].min())
max_year = int(data['Year'].max())
selected_years = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 3. Variable Selector Dropdown
# Providing human-readable variable names mapped to dataframe columns
climate_vars = {
    'Temperature at 2m (T2M) - °C': 'T2M',
    'Maximum Temperature (T2M_MAX) - °C': 'T2M_MAX',
    'Minimum Temperature (T2M_MIN) - °C': 'T2M_MIN',
    'Precipitation (PRECTOTCORR) - mm/day': 'PRECTOTCORR',
    'Relative Humidity (RH2M) - %': 'RH2M',
    'Wind Speed (WS2M) - m/s': 'WS2M'
}
selected_var_name = st.sidebar.selectbox(
    "Select Climate Variable to Visualize:",
    options=list(climate_vars.keys())
)
selected_var = climate_vars[selected_var_name]

# ----------------- Data Filtering -----------------
# Filter by selected countries and year range
filtered_data = data[
    (data['Country'].isin(selected_countries)) &
    (data['Year'] >= selected_years[0]) &
    (data['Year'] <= selected_years[1])
]

if filtered_data.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ----------------- Main Dashboard -----------------

st.markdown("### 📈 Time Series Analysis")
st.markdown(f"**Variable:** {selected_var_name} | **Period:** {selected_years[0]} - {selected_years[1]}")

# Aggregate data by month for smoother line charts
monthly_data = filtered_data.groupby(['Country', pd.Grouper(key='date', freq='ME')])[selected_var].mean().reset_index()

# Plot using Matplotlib/Seaborn for visual consistency with the notebook
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly_data, x='date', y=selected_var, hue='Country', ax=ax)
ax.set_title(f'Monthly Average {selected_var_name}')
ax.set_xlabel('Date')
ax.set_ylabel(selected_var_name.split(' - ')[0])
st.pyplot(fig)


st.markdown("---")
st.markdown("### 📊 Distributions and Boxplots")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{selected_var_name} Distribution across Countries**")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_data, x='Country', y=selected_var, showfliers=False, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

with col2:
    st.markdown("**Summary Statistics**")
    summary_df = filtered_data.groupby('Country')[selected_var].agg(['mean', 'median', 'std', 'max']).reset_index()
    summary_df.columns = ['Country', 'Mean', 'Median', 'Std Dev', 'Max']
    st.dataframe(summary_df.style.format({
        'Mean': '{:.2f}',
        'Median': '{:.2f}',
        'Std Dev': '{:.2f}',
        'Max': '{:.2f}'
    }))

# Extreme Events Section
if selected_var in ['T2M', 'T2M_MAX', 'PRECTOTCORR']:
    st.markdown("---")
    st.markdown("### 🚨 Extreme Events Highlights")
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.markdown("**Extreme Heat Days (> 35°C)**")
        heat_days = filtered_data[filtered_data['T2M_MAX'] > 35].groupby(['Country', 'Year']).size().reset_index(name='Heat Days')
        if not heat_days.empty:
            avg_heat = heat_days.groupby('Country')['Heat Days'].mean().reset_index()
            st.bar_chart(avg_heat.set_index('Country'))
        else:
            st.info("No extreme heat days (> 35°C) found in the selected range.")
            
    with col_e2:
        st.markdown("**Average Dry Days (< 1 mm precipitation)**")
        dry_days = filtered_data[filtered_data['PRECTOTCORR'] < 1].groupby(['Country', 'Year']).size().reset_index(name='Dry Days')
        if not dry_days.empty:
            avg_dry = dry_days.groupby('Country')['Dry Days'].mean().reset_index()
            st.bar_chart(avg_dry.set_index('Country'))
        else:
            st.info("No dry days found in the selected range.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Deployment Note:**")
st.sidebar.caption("This app is ready to be deployed to Streamlit Community Cloud. Ensure your `requirements.txt` includes `streamlit`, `pandas`, `matplotlib`, and `seaborn`.")
