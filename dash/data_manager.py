import pandas as pd
import csv
import os
from typing import ClassVar, List, Any

class DataManager:
    DATA_PATH: ClassVar[str] = "./data/data.csv"
    SAVINGS_PATH: ClassVar[str] = "./data/savings.csv"

    @staticmethod
    def check_if_exist(file_name: str)-> None:
        if not os.path.exists(file_name):
            with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                writer: Any = csv.writer(file, lineterminator="\n")
                writer.writerow(["value", "type", "reason", "day", "month", "year"])

    @staticmethod
    def write(file_name: str, data: List)-> None:
        DataManager.check_if_exist(file_name)

        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer: Any = csv.writer(file, lineterminator="\n")
            writer.writerow(data)

    @staticmethod
    def read_file(file_name: str=DATA_PATH)-> pd.DataFrame:
        DataManager.check_if_exist(file_name)

        return pd.read_csv(file_name)
    
    @staticmethod
    def read_savings()-> pd.DataFrame:
        return DataManager.read_file(DataManager.SAVINGS_PATH)