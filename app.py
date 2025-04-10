import streamlit as st
import json
import os
from datetime import datetime

ARQUIVO_HISTORICO = "historico_compras.json"

# Inicializa sessão
if 'saldo_vr' not in st.session_state:
    st.session_state.saldo_vr = 0.0
if 'produtos' not in st.session_state:
    st.session_state.produtos = []

st.title("🧾 Calculadora de Compras com VR")

# --- SALDO VR ---
saldo_input = st.number_input("Informe seu saldo no VR:", min_value=0.0, step=0.01, value=st.session_state.saldo_vr)
if st.button("Definir saldo"):
    st.session_state.saldo_vr = saldo_input
    st.success(f"Saldo atualizado para R$ {saldo_input:.2f}")

st.markdown("---")

# --- ADICIONAR PRODUTO ---
col1, col2 = st.columns(2)
quantidade = col1.number_input("Quantidade", min_value=1, step=1)
preco_unitario = col2.number_input("Preço unitário (R$)", min_value=0.0, step=0.01)

if st.button("Adicionar produto"):
    st.session_state.produtos.append({
        "quantidade": quantidade,
        "preco_unitario": preco_unitario
    })
    st.success("Produto adicionado!")

# --- LISTA DE PRODUTOS ---
total = 0.0
st.subheader("Produtos adicionados")
if st.session_state.produtos:
    for i, p in enumerate(st.session_state.produtos):
        subtotal = p['quantidade'] * p['preco_unitario']
        total += subtotal
        st.write(f"{i+1}. {p['quantidade']} x R${p['preco_unitario']:.2f} → R${subtotal:.2f}")
else:
    st.info("Nenhum produto adicionado ainda.")

st.markdown("---")

# --- TOTAL E SALDO RESTANTE ---
saldo_restante = st.session_state.saldo_vr - total
st.metric("Total da compra", f"R$ {total:.2f}")
st.metric("Saldo restante no VR", f"R$ {saldo_restante:.2f}")

# --- REMOVER PRODUTO ---
if st.session_state.produtos:
    index_remover = st.number_input("Número do item para remover", min_value=1, max_value=len(st.session_state.produtos), step=1)
    if st.button("Remover produto"):
        st.session_state.produtos.pop(index_remover - 1)
        st.success("Produto removido.")

# --- FINALIZAR COMPRA ---
def salvar_historico():
    mes_atual = datetime.now().strftime("%Y-%m")
    nova_compra = st.session_state.produtos.copy()

    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as f:
            historico = json.load(f)
    else:
        historico = {}

    historico.setdefault(mes_atual, []).extend(nova_compra)

    with open(ARQUIVO_HISTORICO, "w") as f:
        json.dump(historico, f, indent=2)

    st.success(f"Compra salva no histórico de {mes_atual}!")

if st.button("Finalizar compra"):
    if st.session_state.produtos:
        salvar_historico()
        st.session_state.produtos.clear()
        st.success("Compra finalizada e produtos limpos.")
    else:
        st.warning("Adicione produtos antes de finalizar.")
