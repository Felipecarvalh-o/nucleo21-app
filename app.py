import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import random

from engine import processar_fechamento, gerar_jogos
from historico import (
    registrar_analise,
    gerar_ranking,
    listar_analises_usuario,
    resumo_por_estrategia
)
from utils import converter_lista
from fechamentos import FECHAMENTOS
from simulador import simular_cenario

st.set_page_config("Núcleo 21", "🍀", layout="centered")

# ---------------- ESTILO GLOBAL (Mega-Sena Inspired) ----------------
st.markdown("""
<style>
body { background-color:#f6fbf8; }
h1,h2,h3 { color:#1E8449; }

.numero-verde {
    background:#1E8449;
    color:white;
    text-align:center;
    padding:12px;
    border-radius:14px;
    font-size:20px;
    font-weight:700;
    box-shadow:0 4px 10px rgba(0,0,0,0.15);
}
.numero-azul {
    background:#2471A3;
    color:white;
    text-align:center;
    padding:10px;
    border-radius:12px;
    font-size:16px;
    box-shadow:0 3px 8px rgba(0,0,0,0.15);
}
div.stButton > button {
    background:#1E8449;
    color:white;
    border-radius:10px;
    font-weight:bold;
}
div.stButton > button:hover {
    background:#145A32;
}
</style>
""", unsafe_allow_html=True)

# ---------------- ESTRATÉGIAS ----------------
ESTRATEGIAS = {
    "nucleo": {
        "label": "🟢 Núcleo Inteligente™",
        "descricao": (
            "Estratégia analítica adaptativa que identifica a melhor linha "
            "do fechamento e gera jogos otimizados com apoio estatístico."
        )
    },
    "matriz": {
        "label": "🔵 Matriz de Cobertura™",
        "descricao": (
            "Estratégia de organização matemática que prioriza "
            "cobertura ampla e distribuição equilibrada."
        )
    }
}

# ---------------- ESTADO ----------------
for k, v in {
    "logado": False,
    "usuario": "",
    "analise_pronta": False,
    "resultado_sim": None
}.items():
    st.session_state.setdefault(k, v)

# ---------------- LOGIN ----------------
if not st.session_state.logado:
    st.title("🔐 Acesso ao Núcleo 21")
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
    st.caption("1️⃣ Estratégia  |  2️⃣ Resultado  |  3️⃣ Jogos")

    fechamento_nome = st.selectbox("Fechamento", list(FECHAMENTOS.keys()))
    estrategia_key = st.selectbox(
        "🧠 Estratégia",
        list(ESTRATEGIAS.keys()),
        format_func=lambda k: ESTRATEGIAS[k]["label"]
    )
    st.info(ESTRATEGIAS[estrategia_key]["descricao"])
    st.write(f"👤 **{st.session_state.usuario}**")

# ---------------- APP ----------------
st.title("🍀 Núcleo 21")
st.warning("Ferramenta educacional e estatística. Não garante prêmios.")

resultado_txt = st.text_input(
    "Resultado do sorteio (6 dezenas)",
    placeholder="01 02 03 04 05 06"
)

if st.button("🔍 Analisar"):
    resultado = converter_lista(resultado_txt)
    if len(resultado) != 6:
        st.error("Digite exatamente 6 dezenas")
        st.stop()

    pool = list(range(1, 61))
    fechamento = FECHAMENTOS[fechamento_nome]

    if estrategia_key == "nucleo":
        _, melhor = processar_fechamento(pool, resultado, fechamento)
        registrar_analise(
            st.session_state.usuario,
            fechamento_nome,
            resultado,
            melhor["pontos"],
            melhor["numeros"],
            estrategia_key
        )
        st.session_state.melhor = melhor
        st.session_state.jogos = gerar_jogos(melhor["numeros"])
    else:
        nums = list(range(1, 61))
        random.shuffle(nums)
        st.session_state.jogos = [
            sorted(nums[i:i+6]) for i in range(0, 60, 6)
        ]

    st.session_state.analise_pronta = True
    st.session_state.resultado_sim = None

# ---------------- RESULTADOS ----------------
if st.session_state.analise_pronta:
    st.subheader("🎯 Resultado")

    if estrategia_key == "nucleo":
        cols = st.columns(6)
        for c, n in zip(cols, sorted(st.session_state.melhor["numeros"])):
            c.markdown(f"<div class='numero-verde'>{n:02d}</div>", unsafe_allow_html=True)
        st.caption(f"Pontos: **{st.session_state.melhor['pontos']}**")

    st.subheader("🎲 Jogos Gerados")
    for i, jogo in enumerate(st.session_state.jogos, 1):
        cols = st.columns(6)
        for c, n in zip(cols, jogo):
            c.markdown(f"<div class='numero-azul'>{n:02d}</div>", unsafe_allow_html=True)
        st.caption(f"Jogo {i}")

    # -------- EXPORTAÇÃO PREMIUM --------
    st.subheader("📥 Exportar Jogos (Premium)")
    df_export = pd.DataFrame({
        "Jogo": range(1, len(st.session_state.jogos)+1),
        "Dezenas": [" ".join(f"{n:02d}" for n in j) for j in st.session_state.jogos]
    })

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_export.to_excel(writer, index=False, sheet_name="Jogos")
    buffer.seek(0)

    st.download_button(
        "⬇️ Baixar Jogos em Excel",
        buffer,
        "nucleo21_jogos.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ---------------- RANKING ----------------
st.divider()
st.subheader("🏅 Ranking Geral")
ranking = gerar_ranking()
if ranking:
    st.dataframe(
        pd.DataFrame(ranking).sort_values("media", ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Ainda não há dados suficientes.")
