import pandas as pd
import time
from typing import List
import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure
from data_manager import DataManager

class Components:
    @staticmethod
    def expense_pie()-> Figure:
        DataManager.check_if_exist(DataManager.DATA_PATH)

        df: pd.DataFrame = DataManager.read_file()
        
        colors: List[str] = ["#A5B3FF",
                    "#5479F7",
                    "#2739C2",
                    "#7A5CFA",
                    "#9D4EDD",
                    "#C77DFF",
                    "#E0AAFF"]
         
        df = df[df['type'] == 'Despesa']

        if df.empty:
            fig: Figure = go.Figure(go.Pie())
            fig.add_annotation(
                text="Nenhum dado disponível",
                showarrow=False,
                font=dict(size=21)
            )
            return fig

        grouped: pd.Series = df.groupby('reason')['value'].sum()

        fig: Figure = go.Figure(data=[go.Pie(labels=grouped.index.tolist(), 
                                    values=grouped.values.tolist(), 
                                    insidetextorientation='radial',
                                    hole=.4)])
        
        fig.update_traces(hoverinfo='label+percent',
                        textinfo='percent', 
                        textfont_size=20,
                        marker=dict(
                            colors=colors, line=dict(color='#000000', width=2)))

        return fig

    @staticmethod
    def to_str(indexes: List[int])-> List[str]:
        month: List[str] = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]

        str_list: List[str] = []

        for i in indexes:
            str_list.append(month[i - 1])

        return str_list
    
    @staticmethod
    def expense_types_graphics(expense_type)-> Figure:
        DataManager.check_if_exist(DataManager.DATA_PATH)

        df: pd.DataFrame = DataManager.read_file()
        current_year: int = pd.Timestamp.now().year

        df_current: pd.DataFrame = df[(df['year'] == current_year) &
                        (df['reason'] == expense_type)]
        
        if df_current.empty:
            fig: Figure = go.Figure()
            fig.update_layout(height=353) 
            fig.add_annotation(
                text="Nenhum dado disponível",
                showarrow=False,
                font=dict(size=20)
            )
            return fig
        

        grouped: pd.Series = df_current.groupby('month')['value'].sum()

        fig: Figure = go.Figure(go.Scatter(
                        mode="markers+lines", 
                        x=Components.to_str(grouped.index.tolist()), 
                        y=grouped.values.tolist()
                    ))
        
        fig.update_layout(height=353) 

        return fig

    @staticmethod
    def expenses_vs_income()-> Figure:
        DataManager.check_if_exist(DataManager.DATA_PATH)

        current_year: int = pd.Timestamp.now().year
        df: pd.DataFrame = DataManager.read_file()

        df_current: pd.DataFrame = df[df['year'] == current_year]

        if df_current.empty:
            fig: Figure= go.Figure()
            fig.update_layout(height=353) 
            fig.add_annotation(
                text="Nenhum dado disponível",
                showarrow=False,
                font=dict(size=21)
            )
            return fig

        grouped: pd.DataFrame = df_current.groupby(['month', 'type'])['value'].sum().unstack(fill_value=0)

        if 'Receita' not in grouped:
            grouped['Receita'] = 0
        if 'Despesa' not in grouped:
            grouped['Despesa'] = 0

        grouped = grouped.sort_index()

        grouped["Despesa"] = grouped["Despesa"] * -1

        average = grouped["Receita"] + grouped["Despesa"]
        average = average.cumsum()

        fig: Figure = go.Figure()

        fig.add_trace(go.Scatter(
                        x=Components.to_str(grouped.index.tolist()),
                        y=average.values.tolist(),
                        name="Saldo do mês",
                        marker_color="white"

        ))

        fig.add_trace(go.Bar(
                        x=Components.to_str(grouped.index.tolist()), 
                        y=grouped["Receita"].tolist(),
                        name="Receita",
                        marker_color="#2739C2"
                    ))
        
        fig.add_trace(go.Bar(
                        
                        x=Components.to_str(grouped.index.tolist()), 
                        y=grouped["Despesa"].tolist(),
                        name="Despesa",
                        marker_color="#A5B3FF"
                    ))
        
        fig.update_layout(
            barmode='relative',
            bargap=0.7,
            height=500
        )
    
        return fig
