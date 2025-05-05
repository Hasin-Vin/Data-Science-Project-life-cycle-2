# --- 1. Imports and Config ---
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Admin4 Visualization", page_icon="📊", layout="wide")

# --- 2. Load CSV ---
file_path = "https://raw.githubusercontent.com/Hasin-Vin/Data-Science-Project-life-cycle-2/main/cleaned_admin4_data.csv"
try:
    admin4_df = pd.read_csv(file_path)
    st.success("✅ CSV file loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading CSV: {e}")

# --- 3. Data Preview ---
st.subheader("📄 Data Preview")
if not admin4_df.empty:
    st.write("Columns in dataset:", admin4_df.columns.tolist())  # Display all column names
    st.dataframe(admin4_df.head())  # Display first few rows
else:
    st.warning("⚠️ No data to display.")

# --- 4. Check for 'Record_Date' and 'Admin3_Name_En' columns ---
if 'Record_Date' not in admin4_df.columns:
    st.warning("⚠️ 'Record_Date' column not found.")
if 'Admin3_Name_En' not in admin4_df.columns:
    st.warning("⚠️ 'Admin3_Name_En' column not found.")

# --- 5. Extract Year from 'Record_Date' ---
if 'Record_Date' in admin4_df.columns:
    admin4_df['Year'] = pd.to_datetime(admin4_df['Record_Date'], errors='coerce').dt.year
    admin4_df = admin4_df.dropna(subset=['Year'])  # Drop rows where year couldn't be parsed
else:
    st.warning("⚠️ 'Record_Date' column not found, skipping Year extraction.")

# --- 6. Bar Chart (Distribution of Admin4 Areas by Province) ---
st.subheader("📊 Distribution of Admin4 Areas by Province (Bar Chart)")
admin4_counts = admin4_df['Admin1_Name_En'].value_counts().reset_index()
admin4_counts.columns = ['Province', 'Admin4_Count']

bar_fig = px.bar(
    admin4_counts,
    x='Province',
    y='Admin4_Count',
    title='Distribution of Admin4 Areas per Province (Bar Chart)',
    labels={'Province': 'Province', 'Admin4_Count': 'Count of Admin4 Areas'},
    color='Province',
    color_discrete_sequence=px.colors.qualitative.Set2
)
bar_fig.update_layout(
    xaxis_tickangle=45,
    xaxis_title='Province',
    yaxis_title='Count of Admin4 Areas',
    height=600
)
st.plotly_chart(bar_fig, use_container_width=True)

# --- 7. Pie Chart (Distribution of Admin4 Areas by Province) ---
st.subheader("🥧 Distribution of Admin4 Areas (Pie Chart)")
pie_fig = px.pie(
    admin4_counts,
    names='Province',
    values='Admin4_Count',
    title='Distribution of Admin4 Areas per Province'
)
st.plotly_chart(pie_fig, use_container_width=True)

# --- 8. Treemap (Distribution of Admin4 Areas by Province) ---
st.subheader("🌲 Treemap of Admin4 Areas by Province")
treemap_fig = px.treemap(
    admin4_counts,  # Use admin4_counts for the Treemap
    path=['Province'],
    values='Admin4_Count',
    title='Treemap of Admin4 Areas by Province'
)
st.plotly_chart(treemap_fig, use_container_width=True)

# --- 9. Bubble Chart (Top 50 Districts by Simulated Area) ---
st.subheader("💥 Districts Bubble Chart (Top 50 by Simulated Area)")
if 'Admin4_Name_En' in admin4_df.columns:
    np.random.seed(42)
    admin4_df['Simulated_Area'] = np.random.randint(100, 10000, size=len(admin4_df))

    top_bubbles = admin4_df.nlargest(50, 'Simulated_Area').copy()
    top_bubbles['Y_Pos'] = top_bubbles['Simulated_Area'].rank(method='first')

    bubble_fig = px.scatter(
        top_bubbles,
        x='Simulated_Area',
        y='Y_Pos',
        size='Simulated_Area',
        text='Admin4_Name_En',
        title='Top 50 Districts Bubble Chart (Simulated Area)',
        color='Simulated_Area',
        color_continuous_scale='Viridis',
        size_max=15  # Smaller bubbles
    )
    bubble_fig.update_traces(textposition='top center')
    bubble_fig.update_layout(
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        xaxis_title='Simulated Area',
        height=700
    )
    st.plotly_chart(bubble_fig, use_container_width=True)
else:
    st.warning("⚠️ 'Admin4_Name_En' column not found for the Bubble Chart.")

# --- 10. Scatter Plot of Simulated Area vs Population by District ---
st.subheader("📍 Scatter Plot of Simulated Area vs Population by District")

# Generate Simulated Population if not already present
if 'Simulated_Population' not in admin4_df.columns:
    admin4_df['Simulated_Population'] = np.random.randint(1000, 100000, size=len(admin4_df))

scatter_fig = px.scatter(
    admin4_df,
    x='Simulated_Area',
    y='Simulated_Population',
    color='Admin4_Name_En',  # Coloring by district
    hover_name='Admin4_Name_En',
    title='Simulated Area vs Population Colored by District',
    size='Simulated_Population',
    labels={
        'Simulated_Area': 'Simulated Area (km²)',
        'Simulated_Population': 'Simulated Population'
    }
)
scatter_fig.update_layout(height=600, showlegend=False)
st.plotly_chart(scatter_fig, use_container_width=True)

# --- 11. Line Chart (dummy growth example) ---
st.subheader("📈 Dummy Line Chart Example")
line_data = pd.DataFrame({
    'Year': list(range(2015, 2026)),
    'Admin4_Count': np.random.randint(50, 100, size=11)
})
line_fig = px.line(
    line_data,
    x='Year',
    y='Admin4_Count',
    title='Dummy Admin4 Growth Over Time',
    markers=True
)
st.plotly_chart(line_fig, use_container_width=True)

# --- 12. Treemap of Administrative Hierarchy ---
st.subheader("🧱 Treemap of Administrative Hierarchy")

# Ensure the required columns exist
if 'Admin1_Name_En' in admin4_df.columns and 'Admin3_Name_En' in admin4_df.columns and 'Admin4_Name_En' in admin4_df.columns:
    treemap_fig = px.treemap(
        admin4_df,
        path=['Admin1_Name_En', 'Admin3_Name_En', 'Admin4_Name_En'],
        title='Treemap: Province > District > Admin4 Area',
        color='Admin1_Name_En',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(treemap_fig, use_container_width=True)
else:
    st.warning("⚠️ Some required columns ('Admin1_Name_En', 'Admin3_Name_En', 'Admin4_Name_En') are missing for the Treemap.")
