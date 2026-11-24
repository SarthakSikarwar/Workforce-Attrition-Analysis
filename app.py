from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

CLEAN_PATH = Path("dataset/cleaned_employee_attrition.csv")
RAW_PATH = Path("dataset/employee_attrition.csv")

st.set_page_config(
    page_title="Workforce Attrition Analysis",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    path = CLEAN_PATH if CLEAN_PATH.exists() else RAW_PATH
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "Attrition" not in df.columns:
        return None
    if df["Attrition"].dtype == "object":
        mapping = {"yes": 1, "no": 0, "1": 1, "0": 0,
                   "true": 1, "false": 0}
        df["Attrition"] = (
            df["Attrition"].astype(str).str.strip().str.lower().map(mapping)
        )
    df["Attrition"] = pd.to_numeric(df["Attrition"], errors="coerce")
    df = df.dropna(subset=["Attrition"])
    df["Attrition"] = df["Attrition"].astype(int)
    return df

st.title("Workforce Attrition Patterns & Risk Hotspot Analysis")
st.caption("Diagnostic workforce analytics dashboard")

df = load_data()
if df is None:
    st.error(
        "Dataset not found or Attrition column missing. Add "
        "`dataset/employee_attrition.csv`, then run `python data_cleaning.py`."
    )
    st.stop()

filtered = df.copy()

with st.sidebar:
    st.header("Dashboard filters")
    if "Department" in df.columns:
        departments = sorted(df["Department"].dropna().astype(str).unique())
        selected_departments = st.multiselect(
            "Department", departments, default=departments
        )
        filtered = filtered[filtered["Department"].astype(str).isin(selected_departments)]

    if "JobRole" in filtered.columns:
        roles = sorted(filtered["JobRole"].dropna().astype(str).unique())
        selected_roles = st.multiselect("Job role", roles, default=roles)
        filtered = filtered[filtered["JobRole"].astype(str).isin(selected_roles)]

    if "OverTime" in filtered.columns:
        overtime_values = sorted(filtered["OverTime"].dropna().astype(str).unique())
        selected_overtime = st.multiselect(
            "Overtime", overtime_values, default=overtime_values
        )
        filtered = filtered[filtered["OverTime"].astype(str).isin(selected_overtime)]

    if "YearsAtCompany" in filtered.columns and not filtered.empty:
        min_year = int(filtered["YearsAtCompany"].min())
        max_year = int(filtered["YearsAtCompany"].max())
        if min_year < max_year:
            tenure = st.slider(
                "Years at company", min_year, max_year, (min_year, max_year)
            )
            filtered = filtered[
                filtered["YearsAtCompany"].between(tenure[0], tenure[1])
            ]

total = len(filtered)
left = int(filtered["Attrition"].sum()) if total else 0
retained = total - left
rate = left / total * 100 if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Employees in selection", f"{total:,}")
c2.metric("Employees left", f"{left:,}")
c3.metric("Employees retained", f"{retained:,}")
c4.metric("Attrition rate", f"{rate:.2f}%")

st.divider()

if filtered.empty:
    st.warning("No employees match the selected filters.")
    st.stop()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Attrition distribution")
    distribution = (
        filtered["Attrition"].map({0: "Retained", 1: "Left"})
        .value_counts().rename_axis("Status").reset_index(name="Employees")
    )
    fig = px.pie(distribution, names="Status", values="Employees", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Attrition by department")
    if "Department" in filtered.columns:
        dept = (
            filtered.groupby("Department")["Attrition"]
            .agg(employees="size", attrition_rate="mean")
            .reset_index()
        )
        dept["attrition_rate"] *= 100
        fig = px.bar(
            dept, x="Department", y="attrition_rate",
            hover_data=["employees"], labels={"attrition_rate": "Attrition rate (%)"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Department column is not available.")

st.subheader("Attrition by job role")
if "JobRole" in filtered.columns:
    role = (
        filtered.groupby("JobRole")["Attrition"]
        .agg(employees="size", attrition_rate="mean")
        .reset_index()
    )
    role["attrition_rate"] *= 100
    fig = px.bar(
        role.sort_values("attrition_rate", ascending=False),
        x="JobRole", y="attrition_rate", hover_data=["employees"],
        labels={"attrition_rate": "Attrition rate (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Employee records in current selection")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_employee_attrition.csv",
    mime="text/csv"
)

st.caption(
    "Interpretation: group-level attrition rates show association, not causation. "
    "Inspect employee counts before treating a group as a risk hotspot."
)
