import pandas as pd

def detect_delays(df):
    # Standardize columns (case-insensitive matching)
    col_mappings = {}
    for col in df.columns:
        lower_col = col.lower()
        if "shipment" in lower_col and "id" in lower_col:
            col_mappings["shipment_id"] = col
        elif "expected" in lower_col and "deliver" in lower_col:
            col_mappings["expected_date"] = col
        elif "actual" in lower_col and "deliver" in lower_col:
            col_mappings["actual_date"] = col
        elif "expected" in lower_col:
            col_mappings.setdefault("expected_date", col)
        elif "actual" in lower_col:
            col_mappings.setdefault("actual_date", col)

    # Validate presence
    required_keys = ["shipment_id", "expected_date", "actual_date"]
    for key in required_keys:
        if key not in col_mappings:
            raise ValueError(f"Missing required column for {key} detection.")

    # Rename columns for processing
    df = df.rename(columns={
        col_mappings["shipment_id"]: "Shipment ID",
        col_mappings["expected_date"]: "Expected Delivery Date",
        col_mappings["actual_date"]: "Actual Delivery Date"
    })

    # Parse dates
    df["Expected Delivery Date"] = pd.to_datetime(df["Expected Delivery Date"], errors='coerce')
    df["Actual Delivery Date"] = pd.to_datetime(df["Actual Delivery Date"], errors='coerce')

    # Detect delays
    delayed_df = df[df["Actual Delivery Date"] > df["Expected Delivery Date"]]

    return delayed_df[["Shipment ID", "Expected Delivery Date", "Actual Delivery Date"]]
