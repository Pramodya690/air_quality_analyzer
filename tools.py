import json
import os
import glob
import pandas as pd

field_mapping = {
    "co2": ["co2", "CO2 (ppm)", "CO2"],
    "temperature": ["Temperature (\u00b0C)", "temp", "Temp"],
    "humidity": ["Relative Humidity (%)", "rh", "RH"],
}

def normalize_field(name, record):
    try:
        for key, aliases in field_mapping.items():
            for alias in aliases:
                if alias in record:
                    record[key] = record[alias]
                    break
        return {k: record.get(k) for k in ["timestamp", "co2", "temperature", "humidity"]}
    except Exception as e:
        print(f"Error normalizing record: {record}, Error: {e}")
        return {}


def load_all_data(data_dir="data"):
    data = {}
    for filepath in glob.glob(f"{data_dir}/room*.ndjson"):
        room_name = os.path.splitext(os.path.basename(filepath))[0]
        try:
            with open(filepath, "r") as f:
                lines = []
                for line in f:
                    try:
                        record = json.loads(line)
                        norm = normalize_field(room_name, record)
                        lines.append(norm)
                    except json.JSONDecodeError as jde:
                        print(f"JSON decode error in file {filepath}: {jde}")
                    except Exception as ex:
                        print(f"Unexpected error reading line in {filepath}: {ex}")
                df = pd.DataFrame(lines)
                if "timestamp" in df.columns:
                    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True).dt.tz_convert(None)
                data[room_name] = df
        except Exception as e:
            print(f"Error loading")
    return data

