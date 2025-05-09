 
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# App config
st.set_page_config(page_title="Mental Health Indicators Dashboard", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f8fbff;
        color: #333333;
    }
    .stApp {
        background-color: #f8fbff;
    }
    .sidebar .sidebar-content {
        background-color: #ecf2f9;
    }
    h1, h2, h3 {
        color: #003366;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 6px;
    }
    .stButton>button:hover {
        background-color: #0059b3;
    }
    </style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("mental_health_cleaned.csv")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["About", "Visualizations", "Insights"])

# ------------------ ABOUT PAGE ------------------ #
if page == "About":
    st.title("Mental Health Indicators Dashboard")

    st.markdown("""
    ## Introduction

    Mental health is a critical public health concern, with suicide rates serving as a measurable and urgent indicator of societal well-being. This dashboard provides a clear, data-driven view of mental health trends across time, gender, and countries to support informed decision-making.

    ## Purpose

    This interactive application enables government officials, public health professionals, and researchers to:
    - Identify trends in suicide rates by year, gender, and indicator type
    - Compare mental health indicators across countries
    - Generate insights to guide mental health policies and preventive actions

    ## Data Overview

    - Dataset: Cleaned global mental health data including suicide rates and related indicators
    - Key fields:
        - Year: From early 2000s to recent years
        - Country: Reporting country
        - Gender: Male, Female
        - Indicator: Crude rate, age-standardized rate, etc.
        - Value: Reported suicide rate or related metric

    ## Intended Audience

    - Government agencies (e.g., Ministry of Health)
    - Policy analysts and public health researchers
    - NGOs and institutions focused on mental health
    - Journalists and data communicators

    ## How to Use the App

    Use the left sidebar to navigate:
    - Visualizations: Explore suicide and mental health data through graphs and charts
    - Insights: Read key takeaways and observed patterns
    - Filter charts by selecting a specific year, gender, or indicator to explore meaningful views.

    ---
    This tool promotes data transparency, policy awareness, and evidence-based action in the field of mental health.
    """)

# ------------------ VISUALIZATION PAGE ------------------ #
elif page == "Visualizations":
    st.title("Visual Exploration of Mental Health Data")

    # Sidebar filters
    year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
    gender = st.sidebar.selectbox("Select Gender", df['Gender'].dropna().unique())
    indicator = st.sidebar.selectbox("Select Indicator", df['Indicator'].unique())

    # Filtered data
    filtered = df[(df['Year'] == year) & (df['Gender'] == gender) & (df['Indicator'] == indicator)]

    st.subheader(f"Suicide Rates in {year} ({gender}) — {indicator}")
    st.dataframe(filtered)

    # 1. Line Chart — Suicide Trends Over Time
    st.subheader("Suicide Rate Trend Over Time")
    trend_data = df[(df['Gender'] == gender) & (df['Indicator'] == indicator)]
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=trend_data, x='Year', y='Value', hue='Country', marker='o', ax=ax1)
    ax1.set_ylabel("Rate")
    ax1.set_title(f"{indicator} for {gender} Over Time")
    st.pyplot(fig1)

    # 2. Bar Chart — Gender Comparison for Selected Year
    st.subheader("Gender Comparison in Selected Year")
    gender_data = df[(df['Year'] == year) & (df['Indicator'] == indicator)]
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=gender_data, x='Gender', y='Value', hue='Country', ax=ax2)
    ax2.set_ylabel("Rate")
    ax2.set_title(f"{indicator} by Gender in {year}")
    st.pyplot(fig2)

    # 3. Pie Chart — Average Suicide Rates by Indicator
    st.subheader("Indicator Distribution (Same Year)")
    pie_data = df[df['Year'] == year].groupby('Indicator')['Value'].mean()
    fig3 = pie_data.plot.pie(autopct='%1.1f%%', figsize=(6, 6), title="Average Suicide Rate by Indicator").get_figure()
    st.pyplot(fig3)

    # 4. Heatmap — Suicide Rates by Year and Gender (Aggregate View)
    st.subheader("Heatmap: Year vs Gender Suicide Rates")
    heatmap_data = df.pivot_table(index='Year', columns='Gender', values='Value', aggfunc='mean')
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".1f", ax=ax4)
    ax4.set_title("Average Suicide Rates by Year & Gender")
    st.pyplot(fig4)

# ------------------ INSIGHTS PAGE ------------------ #
elif page == "Insights":
    st.title("Key Insights from the Data")

    st.markdown("### Average Suicide Rates by Gender")
    avg_by_gender = df.groupby('Gender')['Value'].mean().sort_values(ascending=False)
    st.dataframe(avg_by_gender)

    fig1, ax1 = plt.subplots()
    sns.barplot(x=avg_by_gender.index, y=avg_by_gender.values, palette="coolwarm", ax=ax1)
    ax1.set_ylabel("Average Suicide Rate")
    st.pyplot(fig1)

    st.markdown("### Year with Highest Average Suicide Rate")
    year_avg = df.groupby('Year')['Value'].mean()
    max_year = year_avg.idxmax()
    st.write(f"The year with the highest average suicide rate was {max_year}, with a rate of {year_avg[max_year]:.2f}.")

    fig2, ax2 = plt.subplots()
    sns.lineplot(x=year_avg.index, y=year_avg.values, marker='o', ax=ax2)
    ax2.set_ylabel("Average Suicide Rate")
    ax2.set_title("Average Suicide Rate Over the Years")
    st.pyplot(fig2)

    st.markdown("### Top 5 Highest Recorded Values")
    top_indicators = df.sort_values(by="Value", ascending=False).head(5)
    st.dataframe(top_indicators)

    st.markdown("### Notable Patterns and Observations")
    st.info("""
    - Male suicide rates are significantly higher across all indicators.
    - Crude suicide rates report more extreme values than age-standardized ones.
    - Years like 2004–2006 show spikes—potentially tied to real-world stressors.
    - Indicator values vary widely by gender, highlighting need for targeted mental health policy.
    """)
