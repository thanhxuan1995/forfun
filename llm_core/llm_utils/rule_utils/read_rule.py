import os
import pandas as pd

from utils.error_utils import ServerException


def read_raw_data(
    file_path,
    modeCombine=False,
    sheet_name=0,
    engine="openpyxl",
    header=0,
    usecols=None,
    skiprows=0,
    nrows=None,
    dtype=None,
    converters=None,
) -> pd.DataFrame:
    _, file_extension = os.path.splitext(file_path)
    try:
        if file_extension.lower() == ".xlsx":
            with pd.ExcelFile(file_path, engine=engine) as xls:
                df = pd.read_excel(
                    xls,
                    sheet_name=sheet_name,
                    header=header,
                    usecols=usecols,
                    skiprows=skiprows,
                    nrows=nrows,
                    dtype=dtype,
                    converters=converters,
                )
        else:
            raise ValueError("Unsupported file format")

        if modeCombine:
            combined_data = []
            current_row = []

            for _, row in df.iterrows():
                if row.isnull().all():
                    if current_row:
                        combined_data.append(current_row)
                        current_row = []
                else:
                    if current_row:
                        current_row = [
                            f"{a}\n{b}".strip() if pd.notnull(b) else a
                            for a, b in zip(current_row, row)
                        ]
                    else:
                        current_row = row.tolist()

            if current_row:
                combined_data.append(current_row)

            combined_df = pd.DataFrame(combined_data, columns=df.columns)
            return combined_df

        else:
            df = df.dropna(how="all")
            return df

    except UnicodeEncodeError as e:
        raise UnicodeEncodeError(f"Encoding error: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
    except ValueError:
        raise ValueError(f"Error: The file '{file_path}' is not a valid Excel file.")
    except Exception as e:
        raise ServerException(f"An unexpected error occurred: {e}")
