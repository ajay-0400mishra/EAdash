
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data
df = pd.read_csv("EA.csv")

# Page configuration
st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")
st.title("🔍 HR Analytics Dashboard – Employee Attrition Insights")

st.markdown("""This dashboard provides both macro and micro-level insights 
into employee attrition trends using the EA.csv dataset. Use the filters and 
tabs to explore the data through visualizations.""") 

# Sidebar filters
st.sidebar.header("Filter Data")
selected_department = st.sidebar.multiselect("Department", df['Department'].unique(), default=df['Department'].unique())
selected_jobrole = st.sidebar.multiselect("Job Role", df['JobRole'].unique(), default=df['JobRole'].unique())
selected_gender = st.sidebar.multiselect("Gender", df['Gender'].unique(), default=df['Gender'].unique())
selected_overtime = st.sidebar.multiselect("OverTime", df['OverTime'].unique(), default=df['OverTime'].unique())

df_filtered = df[
    (df['Department'].isin(selected_department)) &
    (df['JobRole'].isin(selected_jobrole)) &
    (df['Gender'].isin(selected_gender)) &
    (df['OverTime'].isin(selected_overtime))
]

tab1, tab2, tab3 = st.tabs(["📊 Macro Analysis", "📈 Micro Analysis", "📋 Data Table"])

with tab1:
    st.subheader("1. Attrition Rate by Department")
    st.write("This shows which departments have the highest attrition rate.")
    dept_chart = df_filtered.groupby("Department")["Attrition"].value_counts(normalize=True).unstack().fillna(0) * 100
    dept_chart.plot(kind="bar", stacked=True)
    st.pyplot(plt.gcf())
    plt.clf()

    st.subheader("2. Attrition by Job Role")
    st.write("This chart displays attrition distribution across different job roles.")
    role_chart = df_filtered[df_filtered['Attrition'] == "Yes"]['JobRole'].value_counts()
    fig = px.bar(role_chart, x=role_chart.index, y=role_chart.values, labels={'x':"Job Role", 'y':"Attritions"})
    st.plotly_chart(fig)

    st.subheader("3. Attrition by Business Travel Frequency")
    st.write("Tracks if frequent travel contributes to attrition.")
    fig = px.histogram(df_filtered, x='BusinessTravel', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("4. Gender-wise Attrition")
    st.write("Understand attrition trends based on gender.")
    fig = px.histogram(df_filtered, x='Gender', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("5. Overtime vs Attrition")
    st.write("Employees working overtime show higher attrition trends.")
    fig = px.histogram(df_filtered, x='OverTime', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("6. Department-wise Avg Monthly Income")
    st.write("Shows the average monthly income per department.")
    income_chart = df_filtered.groupby('Department')['MonthlyIncome'].mean().sort_values()
    st.bar_chart(income_chart)

    st.subheader("7. Age Distribution")
    st.write("Age distribution of employees with and without attrition.")
    fig = px.histogram(df_filtered, x='Age', color='Attrition', nbins=20)
    st.plotly_chart(fig)

with tab2:
    st.subheader("8. Work-Life Balance vs Attrition")
    st.write("Highlights the importance of work-life balance in retaining employees.")
    fig = px.box(df_filtered, x='WorkLifeBalance', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig)

    st.subheader("9. Years at Company vs Attrition")
    st.write("Shows how long-tenure affects attrition probability.")
    fig = px.box(df_filtered, x='Attrition', y='YearsAtCompany')
    st.plotly_chart(fig)

    st.subheader("10. Job Satisfaction vs Attrition")
    st.write("Indicates the role of job satisfaction in attrition.")
    fig = px.histogram(df_filtered, x='JobSatisfaction', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("11. Environment Satisfaction vs Attrition")
    st.write("Explores how employees' satisfaction with work environment impacts attrition.")
    fig = px.histogram(df_filtered, x='EnvironmentSatisfaction', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("12. Performance Rating vs Attrition")
    st.write("Check if low/high performers tend to leave more.")
    fig = px.histogram(df_filtered, x='PerformanceRating', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("13. Training Times vs Attrition")
    st.write("Training frequency and its relation to attrition.")
    fig = px.histogram(df_filtered, x='TrainingTimesLastYear', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("14. Relationship Satisfaction vs Attrition")
    st.write("Assesses if personal workplace relationships influence attrition.")
    fig = px.histogram(df_filtered, x='RelationshipSatisfaction', color='Attrition', barmode='group')
    st.plotly_chart(fig)

    st.subheader("15. Attrition Correlation Heatmap")
    st.write("Displays correlation of numeric variables with attrition.")
    df_corr = df_filtered.copy()
    df_corr['Attrition'] = df_corr['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
    corr = df_corr.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr[['Attrition']].sort_values(by='Attrition', ascending=False), annot=True, cmap='coolwarm')
    st.pyplot(fig)

with tab3:
    st.subheader("Complete Filtered Data Table")
    st.dataframe(df_filtered)

    st.markdown(f"**Total Records after Filter:** {df_filtered.shape[0]}")
