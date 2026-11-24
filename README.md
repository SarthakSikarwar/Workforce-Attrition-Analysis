# Workforce Attrition Patterns and Risk Hotspot Analysis

A Python + Streamlit starter project for exploring employee attrition patterns.

## 1. Requirements
- Python 3.10 or newer
- VS Code
- An employee attrition CSV dataset

> Important: The project brief mentions Palo Alto Networks, but the commonly circulated HR attrition sample dataset may be IBM HR Analytics data. Verify the dataset's actual source before presenting results as Palo Alto Networks employee statistics.

## 2. Setup in VS Code (Windows)

Open this folder in VS Code, then open **Terminal → New Terminal**.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Place your CSV file at:

`dataset/employee_attrition.csv`

If your file has a different name, either rename it or update `DATA_PATH` in `data_cleaning.py`, `analysis.py`, and `app.py`.

## 3. Run the project

Clean the dataset:

```bash
python data_cleaning.py
```

Generate analysis tables and charts:

```bash
python analysis.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

The dashboard normally opens at `http://localhost:8501`.

## 4. Expected dataset fields

The starter code expects fields such as:
`Attrition`, `Department`, `JobRole`, `Age`, `OverTime`, `BusinessTravel`,
`YearsAtCompany`, `TotalWorkingYears`, `MonthlyIncome`, `Gender`,
`MaritalStatus`, `Education`, `JobSatisfaction`, `WorkLifeBalance`.

Some fields are optional. The scripts check for required columns and skip analyses when fields are unavailable.

`Attrition` can be `Yes/No`, `1/0`, or boolean-like values. The cleaning script converts it to 1 = left and 0 = stayed.

## 5. Project structure

```text
Workforce_Attrition_Analysis/
├── dataset/
│   └── README_DATASET.txt
├── outputs/
├── reports/
├── data_cleaning.py
├── analysis.py
├── app.py
├── requirements.txt
└── README.md
```

## 6. Interpretation notes
- Attrition rates are calculated within each group: leavers in group / all employees in group.
- A high rate in a very small group may be unstable; always inspect group counts too.
- Observational analysis identifies associations, not proof of causation.
- Do not claim the data belongs to Palo Alto Networks unless the dataset source confirms it.
