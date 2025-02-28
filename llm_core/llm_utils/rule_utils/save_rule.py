import os
import json
import pandas as pd

from fastapi import UploadFile
from utils.error_utils import ServerException
from utils.folder_utils import create_directory
from llm_core.prompt_template import RULE_STANDARD_COLUMN_NAME


def save_raw_to_local(path: str, file: UploadFile) -> str:
    create_directory(path)
    new_path = os.path.join(path, file.filename).replace("\\", "/")
    with open(new_path, "wb+") as file_object:
        file_object.write(file.file.read())
    return new_path


def save_result_to_local(
    std_rule: list[list], sheet_name: list[str], path: str, file: UploadFile
) -> str:
    if len(std_rule) != len(sheet_name):
        raise ServerException(
            f"List rule standard and sheet name not equal, got std_rule {len(std_rule)} and sheet_name {len(sheet_name)}"
        )

    df_list = list()
    for rule in std_rule:
        list_to_df = list()
        for string in rule:
            data = json.loads(string)
            data_ordered = {key: data.get(key, "") for key in RULE_STANDARD_COLUMN_NAME}
            list_to_df.append(data_ordered)
        df_list.append(pd.DataFrame(list_to_df))

    create_directory(path)
    processed_path = os.path.join(path, "processed_" + file.filename).replace("\\", "/")

    try:
        with pd.ExcelWriter(processed_path, engine="openpyxl") as writer:
            for id, df in enumerate(df_list):
                df.to_excel(
                    writer,
                    sheet_name=sheet_name[id],
                    index=False,
                    columns=RULE_STANDARD_COLUMN_NAME,
                )

    except Exception as e:
        raise ServerException(f"Can not save file: {e}")

    finally:
        return processed_path
