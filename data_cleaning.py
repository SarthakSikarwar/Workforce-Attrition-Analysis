from pathlib import Path
import pandas as pd

DATA_PATH = Path("dataset/employee_attrition.csv")
OUTPUT_PATH = Path("dataset/cleaned_employee_attrition.csv")

def normalize_attrition(series: pd.Series) -> pd.Series:
    """Convert common Yes/No, 1/0, and boolean values to 1/0."""
    mapping = {
        "yes": 1, "y": 1, "true": 1, "1": 1,
        "no": 0, "n": 0, "false": 0, "0": 0
    }
    normalized = series.astype(str).str.strip().str.lower().map(mapping)
    # Also support numeric values already represented as 0/1.
    numeric = pd.to_numeric(series, errors="coerce")
    normalized = normalized.fillna(numeric.where(numeric.isin([0, 1])))
    return normalized

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place your CSV at dataset/employee_attrition.csv."
        )

    df = pd.read_csv(DATA_PATH)
    print("Original shape:", df.shape)

    df.columns = df.columns.astype(str).str.strip()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("string").str.strip()

    before = len(df)
    df = df.drop_duplicates()
    print("Duplicate rows removed:", before - len(df))

    if "Attrition" not in df.columns:
        raise ValueError("Required column 'Attrition' was not found.")

    df["Attrition"] = normalize_attrition(df["Attrition"])
    invalid = int(df["Attrition"].isna().sum())
    if invalid:
        print(f"Rows with unknown Attrition values: {invalid}")
        df = df.dropna(subset=["Attrition"])

    df["Attrition"] = df["Attrition"].astype(int)

    print("\nMissing values by column:")
    print(df.isna().sum().sort_values(ascending=False).to_string())
    print("\nAttrition counts (1=left, 0=stayed):")
    print(df["Attrition"].value_counts().sort_index().to_string())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nCleaned dataset saved to: {OUTPUT_PATH}")
    print("Final shape:", df.shape)

if __name__ == "__main__":
    main()
