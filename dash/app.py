import streamlit as st
from typing import List, Any
from components import Components
from data_manager import DataManager
from datetime import date
from kpi import KPI

acount: float = KPI.total_acount()
income: float = KPI.get_income_month()
expenses: float = KPI.get_expense_month()
savings: float = KPI.total_savings()

@st.dialog("Nova despesa")
def expense_dialog()-> None:
    expense_value: float = st.number_input("Valor da despesa", min_value=0.0)
    expense_type: str = st.selectbox('Escolha o tipo da despesa', KPI.EXPENSES_TYPES)
    expense_date: date = st.date_input('Selecione a data da despesa')

    data: List[Any] = [expense_value, "Despesa", expense_type, expense_date]
    if st.button("Salvar"):
        DataManager.write('./data/data.csv', data)
        st.rerun()

@st.dialog("Nova receita")
def income_dialog()-> None:
    income_value: float = st.number_input("Valor da receita", min_value=0.0)
    income_date: date = st.date_input('Selecione a data da receita')

    data: List[Any] = [income_value, "Receita", "N/A", income_date]
    if st.button("Salvar"):
        DataManager.write('./data/data.csv', data)
        st.rerun()

@st.dialog("Mover para poupança")
def savings_dialog()-> None:
    saving_value: float = st.number_input("Valor desejado", min_value=0.0)
    saving_date: date = st.date_input('Selecione a data transação')

    data: List[Any] = [saving_value, "N/A", "N/A", saving_date]
    expense_data: List[Any] = [saving_value, "Despesa", "Outros", saving_date]
    if st.button("Salvar"):
        if acount >= saving_value:
            DataManager.write('./data/savings.csv', data)
            DataManager.write('./data/data.csv', expense_data)
            st.rerun()
        else:
            st.error("Saldo insuficiente!")
         
c1, c2, c3 = st.columns([1.06, 1.02, 7])
with c1:
    if st.button("Adicionar Despesa"):
        expense_dialog()
with c2:
    if st.button("Adicionar Receita"):
        income_dialog()
with c3:
    if st.button("Guardar dinheiro"):
        savings_dialog()

st.markdown("<br>", unsafe_allow_html=True)

st.set_page_config(layout="wide")

c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

with c1:
    with st.container(border=True):
        col1, col2 = st.columns([1, 0.3])
        
        with col1:
            st.markdown("<span style='font-size:30px;'>Saldo na conta</span>", unsafe_allow_html=True)
        
        with col2:
            st.image("assets/money.png", width=50)
        
        st.markdown(f"""
                    <span style="font-size:25px">R$ {acount:.2f}</span>
                    """, 
                    unsafe_allow_html=True)

with c2:
    with st.container(border=True):
        
        col1, col2 = st.columns([1, 0.3])
        
        with col1:
            st.markdown("<span style='font-size:30px;'>Receita do mês</span>", unsafe_allow_html=True)
        
        with col2:
            st.image("assets/up.png", width=50)
        
        st.markdown(f"""
                    <span style="font-size:25px">R$ {income:.2f}</span>
                    """, 
                    unsafe_allow_html=True)
with c3:
    with st.container(border=True):
        col1, col2 = st.columns([1, 0.3])
        
        with col1:
            st.markdown("<span style='font-size:30px;'>Despesa do mês</span>", unsafe_allow_html=True)
        
        with col2:
            st.image("assets/down.png", width=50)
        
        st.markdown(f"""
                    <span style="font-size:25px">R$ {expenses:.2f}</span>
                    """, 
                    unsafe_allow_html=True)
with c4:
    with st.container(border=True):
        col1, col2 = st.columns([1, 0.3])
        
        with col1:
            st.markdown("<span style='font-size:30px;'>Poupança</span>", unsafe_allow_html=True)
        
        with col2:
            st.image("assets/pig.png", width=50)
        
        st.markdown(f"""
                    <span style="font-size:25px">R$ {savings:.2f}</span>
                    """, 
                    unsafe_allow_html=True)
        
st.markdown(f"""
            <div style="margin-bottom: 35px; margin-top: 35px;">
                <span style="font-size:25px;">Despesas por categoria:</span>
            </div>    
            """, 
            unsafe_allow_html=True)

c1, c2, = st.columns([0.8, 1])

type: str = KPI.EXPENSES_TYPES[0]

with c1:
    with st.container(border=True):
        st.plotly_chart(Components.expense_pie())
with c2:
    with st.container(border=True):
        cl1, cl2, cl3, cl4, cl5, cl6, cl7 = st.columns([0.87, 1.16, 1.08, 0.8, 1.04, 0.79, 0.9])

        with cl1:
            if st.button(f"{KPI.EXPENSES_TYPES[0]}"):
                type = KPI.EXPENSES_TYPES[0]
        with cl2:
            if st.button(f"{KPI.EXPENSES_TYPES[1]}"):
                type = KPI.EXPENSES_TYPES[1]
        with cl3:
            if st.button(f"{KPI.EXPENSES_TYPES[2]}"):
                type = KPI.EXPENSES_TYPES[2]
        with cl4:
            if st.button(f"{KPI.EXPENSES_TYPES[3]}"):
                type = KPI.EXPENSES_TYPES[3]
        with cl5:
            if st.button(f"{KPI.EXPENSES_TYPES[4]}"):
                type = KPI.EXPENSES_TYPES[4]
        with cl6:
            if st.button(f"{KPI.EXPENSES_TYPES[5]}"):
                type = KPI.EXPENSES_TYPES[5]
        with cl7:
            if st.button(f"{KPI.EXPENSES_TYPES[6]}"):
                type = KPI.EXPENSES_TYPES[6]

        st.text(type)
        st.plotly_chart(Components.expense_types_graphics(type))

st.markdown(f"""
    <div style="margin-bottom: 35px; margin-top: 35px;">
        <span style="font-size:25px;">Balanço Financeiro Mensal:</span>
    </div>    
    """, 
    unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 0.8])

with col2:
    st.plotly_chart(Components.expenses_vs_income(), use_container_width=False)