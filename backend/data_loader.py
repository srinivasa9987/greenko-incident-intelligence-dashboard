from pathlib import Path
import pandas as pd

DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "safety_esg_incidents.csv")

REQUIRED_COLUMNS = ["incident_id", "narrative", "target_category", "target_severity"]
ALLOWED_CATEGORIES = {"safety", "environment", "esg_compliance"}
ALLOWED_SEVERITIES = {"low", "medium", "high"}
ID_COLUMN = "incident_id"
LABEL_COLUMNS = ["target_category", "target_severity"]
CSV_ROW_OFFSET = 2

def _clean_text(series: pd.Series, lowercase: bool = False) -> pd.Series:
    cleaned = series.fillna("").astype(str).str.strip()
    return cleaned.str.lower() if lowercase else cleaned


def _check_not_blank(series: pd.Series, df: pd.DataFrame, label: str) -> None:
    blank = series.eq("")
    if blank.any():
        rows = (df.index[blank] + CSV_ROW_OFFSET).tolist()
        raise ValueError(f"Missing {label} at CSV rows: {rows}")


def _check_allowed(series: pd.Series, allowed: set, label: str) -> None:
    invalid = sorted(set(series) - allowed)
    if invalid:
        raise ValueError(f"Invalid {label}: {invalid}. Allowed values: {sorted(allowed)}")

def validate_incident_data(df: pd.DataFrame) -> bool:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Incident data must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("The historical incident dataset is empty.")
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    # Incident IDs: present and unique
    ids = _clean_text(df["incident_id"])
    _check_not_blank(ids, df, "incident IDs")
    duplicates = ids[ids.duplicated(keep=False)].unique().tolist()
    if duplicates:
        raise ValueError(f"Duplicate incident IDs found: {duplicates}")
    # Narratives: present
    _check_not_blank(_clean_text(df["narrative"]), df, "incident narratives")
    _check_allowed(_clean_text(df["target_category"], lowercase=True), ALLOWED_CATEGORIES,"incident categories")
    _check_allowed( _clean_text(df["target_severity"], lowercase=True),ALLOWED_SEVERITIES,"severity levels")
    return True

def load_incidents() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Historical incident dataset not found: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    if ID_COLUMN in df.columns:
        df[ID_COLUMN] = df[ID_COLUMN].astype("string").str.strip()
    for column in LABEL_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip().str.lower()
    validate_incident_data(df)
    return df