import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import streamlit as st
from io import BytesIO
import base64

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="📊 Naukri.com Jobs Dashboard and Analysis",
    layout="wide"
)

st.title("📊 Business Analyst Jobs Dashboard")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.sidebar.header("🔧 Column Mapping")

    # Dropdowns for column mapping
    company_col = st.sidebar.selectbox("Company Column", df.columns, index=1)
    location_col = st.sidebar.selectbox("Location Column", df.columns, index=4)
    skills_col = st.sidebar.selectbox("Skills Column", df.columns, index=6)
    desc_col = st.sidebar.selectbox("Description Column", df.columns, index=7)

    # ----------------------------
    # Visualizations
    # ----------------------------

    # 1. Top Companies - Horizontal Bar
    company_df = df[company_col].value_counts().reset_index()
    company_df.columns = ["Company", "Count"]

    fig_company = px.bar(
        company_df.head(20).sort_values("Count", ascending=True),
        x="Count", y="Company",
        orientation="h",
        title="🏢 Top Hiring Companies (Top 20)",
        text="Count",
        color="Count",
        color_continuous_scale=px.colors.sequential.Tealgrn
    )
    fig_company.update_traces(textposition="outside")
    st.plotly_chart(fig_company, use_container_width=True)

    # 2. Top Locations - Treemap
    location_counts = df[location_col].value_counts().reset_index()
    location_counts.columns = ["Location", "Count"]

    fig_location = px.treemap(
        location_counts.head(30),
        path=["Location"], values="Count",
        color="Count",
        color_continuous_scale=px.colors.sequential.Purpor,
        title="🌍 Top Job Locations (Treemap)"
    )
    fig_location.update_traces(
        texttemplate="<b>%{label}</b><br>📌 %{value} jobs<br>({percentParent:.1%})",
        textinfo="label+value+percent parent"
    )
    st.plotly_chart(fig_location, use_container_width=True)

    # 3. Top Skills - Horizontal Bar
    all_skills = []
    for skills_str in df[skills_col].fillna(""):
        skills = [s.strip().lower() for s in str(skills_str).split(",") if s.strip()]
        all_skills.extend(skills)

    skills_series = pd.Series(all_skills).value_counts().head(30)
    skills_df = skills_series.reset_index()
    skills_df.columns = ["Skill", "Count"]

    fig_skills = px.bar(
        skills_df.sort_values("Count", ascending=True),
        x="Count", y="Skill",
        orientation="h",
        title="🛠 Top Skills (Top 30)",
        text="Count",
        color="Count",
        color_continuous_scale=px.colors.sequential.Sunset
    )
    fig_skills.update_traces(textposition="outside")
    st.plotly_chart(fig_skills, use_container_width=True)

    # 4. Word Cloud - Job Descriptions
    st.subheader("☁ Word Cloud - Job Descriptions")
    text_desc = " ".join(df[desc_col].fillna("").astype(str).tolist())
    wordcloud_desc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="coolwarm",
        max_words=200
    ).generate(text_desc)

    img1 = BytesIO()
    wordcloud_desc.to_image().save(img1, format="PNG")
    st.image(img1, use_container_width=True)

    # 5. Word Cloud - Skills
    st.subheader("☁ Word Cloud - Skills")
    text_skills = " ".join(all_skills)
    wordcloud_skills = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="viridis",
        max_words=150
    ).generate(text_skills)

    img2 = BytesIO()
    wordcloud_skills.to_image().save(img2, format="PNG")
    st.image(img2, use_container_width=True)

else:
    st.info("👆 Upload an Excel file to get started.")
