import time
from data_manager import DataManager
from typing import ClassVar, List
import pandas as pd

class KPI:
    EXPENSES_TYPES: ClassVar[List[str]] = [
            "Moradia",
            "Alimentação",
            "Transporte",
            "Saúde",
            "Educação",
            "Lazer",
            "Outros"
        ]
    
    @staticmethod
    def total_acount()-> float:
        DataManager.check_if_exist(DataManager.DATA_PATH)

        df: pd.DataFrame = DataManager.read_file()

        total: pd.Series = df.groupby("type")['value'].sum()

        return total['Receita'] - total['Despesa']

    @staticmethod
    def get_income_month()-> float:
        DataManager.check_if_exist(DataManager.DATA_PATH)
        
        df: pd.DataFrame = DataManager.read_file()

        total: pd.DataFrame = df.groupby([df['date'].dt.to_period('M'), "type"])['value'].sum().unstack(fill_value=0)

        return total["Receita"].iloc[-1]

    @staticmethod
    def get_expense_month()-> float:
        DataManager.check_if_exist(DataManager.DATA_PATH)
        
        df: pd.DataFrame = DataManager.read_file()

        total: pd.DataFrame = df.groupby([df['date'].dt.to_period('M'), "type"])['value'].sum().unstack(fill_value=0)

        return total["Despesa"].iloc[-1]

    @staticmethod
    def total_savings()-> float:
        DataManager.check_if_exist(DataManager.SAVINGS_PATH)

        df: pd.DataFrame = DataManager.read_savings()

        return df["value"].sum()
    