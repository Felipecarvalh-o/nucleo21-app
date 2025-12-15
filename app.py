import streamlit as st
import pandas as pd
import plotly.express as px

from engine import processar_fechamento, gerar_jogos
from historico import (
    registrar_analise,
    gerar_ranking,
    gerar_ranking_por_usuario,
    listar_analises_usuario
)
from utils import converter_lista
from fechamentos import FECHAMENTOS
from simulador import simular_cenario

st.set_page_config("Núcleo 21", "🍀", layout="centered")

# ---------------- ESTADO ----------------
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "analise_pronta" not in st.session_state:
    st.session_state.analise_pronta = False
if "resultado_sim" not in st.session_state:
    st.session_state.resultado_sim = None

# ---------------- LOGIN ----------------
if not st.session_state.logado:
    st.title("🔐 Login")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if u and s:
            st.session_state.logado = True
            st.session_state.usuario = u
            st.rerun()
        else:
            st.error("Informe usuário e senha")
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Configurações")
    fechamento_nome = st.selectbox(
        "Fechamento", list(FECHAMENTOS.keys())
    )
    st.write(f"👤 {st.session_state.usuario}")

# ---------------- APP ----------------
st.title("🍀 Núcleo 21")
resultado_txt = st.text_input(
    "Resultado do sorteio (6 dezenas)",
    placeholder="01 02 03 04 05 06"
)

if st.button("🔍 ANALISAR"):
    resultado = converter_lista(resultado_txt)
    if len(resultado) != 6:
        st.error("Digite exatamente 6 dezenas")
        st.stop()

    pool = list(range(1, 61))
    fechamento = FECHAMENTOS[fechamento_nome]
    _, melhor = processar_fechamento(pool, resultado, fechamento)

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

# ---------------- RESULTADOS ----------------
if st.session_state.analise_pronta:
    st.subheader("🏆 Melhor Linha")
    cols = st.columns(6)
    for c, n in zip(cols, sorted(st.session_state.melhor["numeros"])):
        c.markdown(
            f"<div style='background:#2ecc71;color:white;"
            f"text-align:center;padding:10px;border-radius:8px;"
            f"font-size:18px;font-weight:bold;'>"
            f"{str(n).zfill(2)}</div>",
            unsafe_allow_html=True
        )
    st.caption(f"Pontos: {st.session_state.melhor['pontos']}")

    # -------- SIMULAÇÃO --------
    st.subheader("🧪 Simulação Educacional")
    st.caption(
        "🧪 Simulação educacional baseada em 500 sorteios aleatórios. "
        "Não representa previsões nem garante resultados."
    )

    if st.button("▶️ Simular Estratégia"):
        st.session_state.resultado_sim = simular_cenario(
            st.session_state.jogos, 500
        )

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Máximo", r["maximo"])
        c3.metric("⭐ ≥4", r["acima_4"])
        c4.metric("❌ Zeros", r["zeros"])

# ---------------- EVOLUÇÃO ----------------
st.divider()
st.subheader("📈 Minha Evolução")

dados = listar_analises_usuario(st.session_state.usuario)

if len(dados) >= 2:
    df = pd.DataFrame(dados)
    df["ordem"] = range(1, len(df) + 1)
    df["media_movel"] = df["pontos"].rolling(3).mean()

    fig = px.line(
        df,
        x="ordem",
        y=["pontos", "media_movel"],
        markers=True,
        labels={"value": "Pontos", "ordem": "Análises"},
        title="Evolução de Pontos (com média móvel)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Faça mais análises para visualizar sua evolução.")

# ---------------- RODAPÉ ----------------
st.markdown(
    "<hr><div style='text-align:center;color:gray;font-size:14px;'>"
    "<strong>⚠️ Aviso Legal</strong><br>"
    "Ferramenta educacional e estatística. "
    "Não possui vínculo com a Caixa ou loterias oficiais."
    "</div>",
    unsafe_allow_html=True
)
