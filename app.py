import streamlit as st
import pandas as pd

from engine import processar_fechamento, gerar_jogos
from historico import (
    registrar_analise,
    carregar_historico,
    gerar_ranking,
    gerar_ranking_por_usuario
)
from utils import converter_lista
from fechamentos import FECHAMENTOS

# =============================
# CONFIGURAÇÃO
# =============================
st.set_page_config(
    page_title="Núcleo 21",
    page_icon="🍀",
    layout="centered"
)

# =============================
# ESTADO
# =============================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =============================
# LOGIN
# =============================
if not st.session_state.logado:
    st.title("🔐 Núcleo 21 — Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario and senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Informe usuário e senha")

    st.stop()

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.header("⚙️ Configurações")

    fechamento_nome = st.selectbox(
        "Fechamento",
        list(FECHAMENTOS.keys())
    )

    st.divider()
    st.write(f"👤 Usuário: **{st.session_state.usuario}**")

# =============================
# APP
# =============================
st.title("🍀 Núcleo 21")
st.caption("Ferramenta educacional · Análise estatística")

# =============================
# ENTRADA
# =============================
resultado_text = st.text_input(
    "Resultado do sorteio (6 dezenas)",
    placeholder="05 12 18 32 41 56"
)

if st.button("🔍 ANALISAR AGORA", use_container_width=True):
    resultado = converter_lista(resultado_text)

    if len(resultado) != 6:
        st.error("Digite exatamente 6 dezenas válidas.")
        st.stop()

    pool = list(range(1, 61))
    fechamento = FECHAMENTOS[fechamento_nome]

    linhas, melhor = processar_fechamento(pool, resultado, fechamento)

    registrar_analise(
        st.session_state.usuario,
        fechamento_nome,
        resultado,
        melhor["pontos"],
        melhor["numeros"]
    )

    st.subheader("🏆 Melhor Linha")
    st.success(f"{sorted(melhor['numeros'])} — {melhor['pontos']} pontos")

    st.subheader("🎟️ Sugestões de Jogos")
    for jogo in gerar_jogos(melhor["numeros"]):
        st.write(jogo)

# =============================
# AJUSTE DE ESTRATÉGIA (INTELIGENTE)
# =============================
st.divider()
st.subheader("🧠 Seu Padrão de Resultados")

historico = carregar_historico()
user_data = [h for h in historico if h["usuario"] == st.session_state.usuario]

if len(user_data) >= 3:
    df = pd.DataFrame(user_data)

    media = round(df["score"].mean(), 2)

    melhor_fechamento = (
        df.groupby("fechamento")["score"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )

    st.info(
        f"📊 Sua média de pontos é **{media}**.\n\n"
        f"⭐ Você costuma ter melhores resultados com o "
        f"**Fechamento {melhor_fechamento}**."
    )
else:
    st.info(
        "ℹ️ Faça pelo menos **3 análises** para que eu consiga "
        "identificar seus padrões."
    )

# =============================
# RANKINGS
# =============================
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Ranking Geral")
    ranking = gerar_ranking()
    for i, r in enumerate(ranking, 1):
        st.write(f"{i}º — {r['score']} pts — {r['usuario']}")

with col2:
    st.subheader("👤 Meu Ranking")
    ranking_user = gerar_ranking_por_usuario(st.session_state.usuario)
    for i, r in enumerate(ranking_user, 1):
        st.write(f"{i}º — {r['score']} pts — {r['data']}")
