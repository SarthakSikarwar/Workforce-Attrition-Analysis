from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = Path("dataset/cleaned_employee_attrition.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def group_attrition(df, column):
    result = (
        df.groupby(column, dropna=False)["Attrition"]
        .agg(employees="size", employees_left="sum", attrition_rate="mean")
        .reset_index()
    )
    result["attrition_rate"] = (result["attrition_rate"] * 100).round(2)
    return result.sort_values("attrition_rate", ascending=False)

def save_bar_chart(table, category, title, filename):
    if table.empty:
        return
    plt.figure(figsize=(10, 5))
    sns.barplot(data=table, x=category, y="attrition_rate")
    plt.title(title)
    plt.xlabel(category)
    plt.ylabel("Attrition rate (%)")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close()

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python data_cleaning.py first.")

    df = pd.read_csv(DATA_PATH)
    if "Attrition" not in df:
        raise ValueError("Attrition column is missing.")

    total = len(df)
    left = int(df["Attrition"].sum())
    retained = total - left
    rate = (left / total * 100) if total else 0

    print(f"Total employees: {total}")
    print(f"Employees left: {left}")
    print(f"Employees retained: {retained}")
    print(f"Overall attrition rate: {rate:.2f}%")

    summary = pd.DataFrame([{
        "total_employees": total,
        "employees_left": left,
        "employees_retained": retained,
        "attrition_rate_percent": round(rate, 2)
    }])
    summary.to_csv(OUTPUT_DIR / "overall_kpis.csv", index=False)

    for col in ["Department", "JobRole", "OverTime", "BusinessTravel",
                "Gender", "MaritalStatus", "EducationField"]:
        if col in df.columns:
            table = group_attrition(df, col)
            table.to_csv(OUTPUT_DIR / f"{col.lower()}_attrition.csv", index=False)
            save_bar_chart(
                table, col, f"Attrition rate by {col}",
                f"{col.lower()}_attrition.png"
            )

    if "YearsAtCompany" in df.columns:
        df["TenureGroup"] = pd.cut(
            df["YearsAtCompany"],
            bins=[-1, 2, 5, 10, float("inf")],
            labels=["0-2 years", "3-5 years", "6-10 years", "10+ years"]
        )
        table = group_attrition(df, "TenureGroup")
        table.to_csv(OUTPUT_DIR / "tenure_attrition.csv", index=False)
        save_bar_chart(
            table, "TenureGroup", "Attrition rate by company tenure",
            "tenure_attrition.png"
        )

    print(f"\nAnalysis outputs saved in: {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
