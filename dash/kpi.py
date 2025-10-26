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
        
        current_date: pd.Timestamp = pd.Timestamp.now()
        year: int = current_date.year

        total_income: float = df[
                        (df['year']  == year) &
                        (df['type'] == "Receita")]['value'].sum()

        total_expense: float = df[
                        (df['year']  == year) &
                        (df['type'] == "Despesa")]['value'].sum()

        return total_income - total_expense

    @staticmethod
    def get_income_month()-> float:
        DataManager.check_if_exist(DataManager.DATA_PATH)
        
        df: pd.DataFrame = DataManager.read_file()
        current_date: pd.Timestamp = pd.Timestamp.now()
        month: int = current_date.month
        year: int = current_date.year

        total_income: float = df[
                        (df['month'] == month) &
                        (df['year'] == year) &
                        (df['type'] == "Receita")
                        ]['value'].sum()
            
        return total_income

    @staticmethod
    def get_expense_month()-> float:
        DataManager.check_if_exist(DataManager.DATA_PATH)

        df: pd.DataFrame = DataManager.read_file()
        
        current_date: pd.Timestamp = pd.Timestamp.now()
        month: int = current_date.month
        year: int = current_date.year

        total_expense: float = df[
                        (df['month'] == month) &
                        (df['year'] == year) &
                        (df['type'] == "Despesa")]['value'].sum()

        return total_expense

    @staticmethod
    def total_savings()-> float:
        DataManager.check_if_exist(DataManager.SAVINGS_PATH)

        df: pd.DataFrame = DataManager.read_savings()

        return df["value"].sum()
    