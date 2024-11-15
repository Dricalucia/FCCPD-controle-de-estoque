import streamlit as st
import requests
import pandas as pd
import os

# Usa a variável de ambiente para a URL da API ou fallback para localhost
API_URL = os.getenv("API_URL", "http://web:8000")

def listar_fornecedores():
    try:
        response = requests.get(f"{API_URL}/fornecedores/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Erro ao obter dados de fornecedores.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return []

def deletar_fornecedor(fornecedor_id):
    try:
        response = requests.delete(f"{API_URL}/fornecedores/{fornecedor_id}")
        if response.status_code == 200:
            st.success("Fornecedor deletado com sucesso!")
        else:
            st.error("Erro ao deletar fornecedor.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")

def selecionar_e_deletar_fornecedor():
    
        fornecedores = listar_fornecedores()
        
        if fornecedores:
            fornecedor_opcoes = {
                f"{forn['name']} - {forn['contact']}": forn["id"]
                for forn in fornecedores
            }
            fornecedor_selecionado = st.selectbox(
                "Selecione um fornecedor para deletar", list(fornecedor_opcoes.keys())
            )
            if st.button("Deletar Fornecedor"):
                deletar_fornecedor(fornecedor_opcoes[fornecedor_selecionado])

def listar_ingredientes():
    try:
        response = requests.get(f"{API_URL}/ingredientes/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Erro ao obter dados de ingredientes.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return []

def deletar_ingrediente(ingrediente_id):
    try:
        response = requests.delete(f"{API_URL}/ingredientes/{ingrediente_id}")
        if response.status_code == 200:
            st.success("Ingrediente deletado com sucesso!")
        else:
            st.error("Erro ao deletar ingrediente.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")

def selecionar_e_deletar_ingrediente():

    ingredientes = listar_ingredientes()

    if ingredientes:
        ingrediente_opcoes = {
            f"{ing['name']} - {ing['quantity']} {ing['unit']}": ing["id"]
            for ing in ingredientes
        }
        ingrediente_selecionado = st.selectbox(
            "Selecione um ingrediente para deletar", list(ingrediente_opcoes.keys())
        )

        if st.button("Deletar Ingrediente"):
            deletar_ingrediente(ingrediente_opcoes[ingrediente_selecionado])

def main():

    st.set_page_config(
        page_title="Sistema de Controle de Estoque de Doceria",
        page_icon=":cake:",
        initial_sidebar_state="expanded",
    )

    st.title("Sistema de Controle de Estoque de Doceria")

    menu = ["Fornecedores", "Ingredientes", "Movimentações"]
    choice = st.sidebar.selectbox("Selecione a Operação", menu)

    if choice == "Fornecedores":
        st.subheader("Gestão de Fornecedores")

        # Adicionar novo fornecedor
        with st.form("adicionar_fornecedor"):
            st.write("Adicionar Novo Fornecedor")
            name = st.text_input("Nome")
            contact = st.text_input("Contato")
            email = st.text_input("Email")
            if st.form_submit_button("Adicionar Fornecedor"):
                try:
                    response = requests.post(
                        f"{API_URL}/fornecedores/",
                        json={"name": name, "contact": contact, "email": email},
                    )
                    if response.status_code == 200:
                        st.success("Fornecedor adicionado com sucesso!")
                    else:
                        st.error("Falha ao adicionar fornecedor.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao conectar com a API: {str(e)}")

        # Listar fornecedores
        if st.button("Visualizar Fornecedores"):
            try:
                response = requests.get(f"{API_URL}/fornecedores/")
                if response.status_code == 200:
                    suppliers = response.json()
                    df = pd.DataFrame(suppliers)
                    st.dataframe(df)
                else:
                    st.error("Erro ao obter dados de fornecedores.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")

        # Selecionar e deletar ingredientes
        selecionar_e_deletar_fornecedor()

    elif choice == "Ingredientes":
        st.subheader("Gestão de Ingredientes")

        # Adicionar novo ingrediente
        with st.form("adicionar_ingrediente"):
            st.write("Adicionar Novo Ingrediente")
            name = st.text_input("Nome")
            quantity = st.number_input("Quantidade", min_value=0, step=1)
            unit = st.text_input("Unidade")
            min_stock = st.number_input("Estoque Mínimo", min_value=0, step=1)
            supplier_id = st.number_input("ID do Fornecedor", min_value=1, step=1)
            if st.form_submit_button("Adicionar Ingrediente"):
                try:
                    response = requests.post(
                        f"{API_URL}/ingredientes/",
                        json={
                            "name": name,
                            "quantity": quantity,
                            "unit": unit,
                            "min_stock": min_stock,
                            "supplier_id": supplier_id,
                        },
                    )
                    if response.status_code == 200:
                        st.success("Ingrediente adicionado com sucesso!")
                    else:
                        st.error("Falha ao adicionar ingrediente.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao conectar com a API: {str(e)}")

        # Listar ingredientes
        if st.button("Visualizar Ingredientes"):
            try:
                response = requests.get(f"{API_URL}/ingredientes/")
                if response.status_code == 200:
                    ingredients = response.json()
                    df = pd.DataFrame(ingredients)
                    st.dataframe(df)
                else:
                    st.error("Erro ao obter dados de ingredientes.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")

        # Visualizar ingredientes com estoque baixo
        if st.button("Visualizar Ingredientes com Estoque Baixo"):
            try:
                response = requests.get(f"{API_URL}/ingredientes/estoque-baixo")
                if response.status_code == 200:
                    low_stock = response.json()
                    df = pd.DataFrame(low_stock)
                    st.dataframe(df)
                else:
                    st.error("Erro ao obter dados de estoque baixo.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")

        # Selecionar e deletar ingredientes
        selecionar_e_deletar_ingrediente()

    elif choice == "Movimentações":
        st.subheader("Movimentações de Estoque")

        # Adicionar nova movimentação
        with st.form("adicionar_movimentacao"):
            st.write("Adicionar Movimentação")
            ingredient_id = st.number_input("ID do Ingrediente", min_value=1, step=1)
            movement_type = st.selectbox("Tipo de Movimentação", ["ENTRADA", "SAÍDA"])
            quantity = st.number_input("Quantidade", min_value=0, step=1)
            if st.form_submit_button("Adicionar Movimentação"):
                try:
                    response = requests.post(
                        f"{API_URL}/movimentacoes/",
                        json={
                            "ingredient_id": ingredient_id,
                            "movement_type": movement_type,
                            "quantity": quantity,
                        },
                    )
                    if response.status_code == 200:
                        st.success("Movimentação registrada com sucesso!")
                    else:
                        st.error("Falha ao registrar movimentação.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao conectar com a API: {str(e)}")

        # Listar movimentações
        if st.button("Visualizar Movimentações"):
            try:
                response = requests.get(f"{API_URL}/movimentacoes/")
                if response.status_code == 200:
                    movements = response.json()
                    df = pd.DataFrame(movements)
                    st.dataframe(df)
                else:
                    st.error("Erro ao obter dados de movimentações.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")


if __name__ == "__main__":
    main()
