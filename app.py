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
from simulador import simular_cenario

# =============================
# CONFIGURAÇÃO
# =============================
st.set_page_config(
    page_title="Núcleo 21",
    page_icon="🍀",
    layout="centered"
)

# =============================
# ESTADOS GLOBAIS
# =============================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if "aceitou_termos" not in st.session_state:
    st.session_state.aceitou_termos = False

if "analise_pronta" not in st.session_state:
    st.session_state.analise_pronta = False

if "melhor" not in st.session_state:
    st.session_state.melhor = None

if "jogos" not in st.session_state:
    st.session_state.jogos = []

if "resultado_sim" not in st.session_state:
    st.session_state.resultado_sim = None

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
# ACEITE DE TERMOS (OBRIGATÓRIO)
# =============================
if not st.session_state.aceitou_termos:
    st.title("📄 Termos de Uso e Política de Privacidade")

    st.markdown(
        """
        ### ⚠️ Aviso Importante

        O **Núcleo 21** é uma ferramenta **exclusivamente educacional e estatística**.

        - Não garante ganhos  
        - Não oferece previsões  
        - Não interfere em sorteios oficiais  
        - Jogos de loteria são baseados em **aleatoriedade**

        Ao continuar, você declara que:
        - leu e compreendeu os Termos de Uso
        - está ciente dos riscos envolvidos
        - utiliza o sistema por sua conta e risco
        """
    )

    concordo = st.checkbox(
        "✅ Li e concordo com os Termos de Uso e a Política de Privacidade"
    )

    if st.button("Continuar"):
        if concordo:
            st.session_state.aceitou_termos = True
            st.rerun()
        else:
            st.error("Você precisa concordar para continuar.")

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
# APP PRINCIPAL
# =============================
st.title("🍀 Núcleo 21")
st.caption("Ferramenta educacional · Análise estatística")

st.warning(
    "⚠️ Este aplicativo possui finalidade exclusivamente educacional e estatística. "
    "Não garante ganhos, não oferece previsões e não interfere em sorteios oficiais."
)

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

    st.session_state.melhor = melhor
    st.session_state.jogos = gerar_jogos(melhor["numeros"])
    st.session_state.analise_pronta = True
    st.session_state.resultado_sim = None

# =============================
# RESULTADOS
# =============================
if st.session_state.analise_pronta:
    melhor = st.session_state.melhor
    jogos = st.session_state.jogos

    st.subheader("🏆 Melhor Linha")

    cols = st.columns(6)
    for col, n in zip(cols, sorted(melhor["numeros"])):
        col.markdown(
            f"<div style='text-align:center; padding:10px; border-radius:8px;"
            f"background-color:#2ecc71; color:white; font-weight:bold; font-size:18px;'>"
            f"{str(n).zfill(2)}</div>",
            unsafe_allow_html=True
        )

    st.caption(f"🎯 Pontuação: **{melhor['pontos']} pontos**")

    st.subheader("🎟️ Sugestões de Jogos")

    for jogo in jogos:
        cols = st.columns(6)
        for col, n in zip(cols, jogo):
            col.markdown(
                f"<div style='text-align:center; padding:8px; border-radius:6px;"
                f"background-color:#2ecc71; color:white; font-weight:bold;'>"
                f"{str(n).zfill(2)}</div>",
                unsafe_allow_html=True
            )
        st.write("")

    # =============================
    # SIMULAÇÃO
    # =============================
    st.divider()
    st.subheader("🧪 Simulação de Cenários (Educacional)")

    if st.button("▶️ Simular Estratégia", use_container_width=True):
        st.session_state.resultado_sim = simular_cenario(jogos, simulacoes=500)

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim

        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Média de Pontos", r["media"])
            st.metric("🏆 Máximo Obtido", r["maximo"])
        with col2:
            st.metric("❌ Vezes que Zerou", r["zeros"])
            st.metric("⭐ Pontuações ≥ 4", r["acima_4"])

# =============================
# RODAPÉ
# =============================
st.markdown(
    "<hr style='margin-top:40px;'>"
    "<div style='text-align:center; font-size:14px; color:gray; line-height:1.8;'>"
    "<div style='font-size:22px;'>⚠️</div>"
    "<strong>Aviso Legal</strong><br>"
    "Ferramenta educacional e estatística. "
    "Não garante ganhos nem oferece previsões."
    "</div>",
    unsafe_allow_html=True
)
