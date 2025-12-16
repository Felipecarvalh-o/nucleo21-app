import streamlit as st
import pandas as pd
import plotly.express as px

from engine import processar_fechamento, gerar_jogos
from historico import registrar_analise, gerar_ranking
from utils import converter_lista
from fechamentos import FECHAMENTOS
from simulador import simular_cenario

st.set_page_config("Núcleo 21", "🍀", layout="centered")

# ---------------- ESTILO GLOBAL ----------------
st.markdown(
    """
    <style>
    .numero-verde {
        background:#1E8449;
        color:white;
        text-align:center;
        padding:12px;
        border-radius:12px;
        font-size:20px;
        font-weight:700;
        box-shadow:0 4px 8px rgba(0,0,0,0.15);
        margin-bottom:4px;
    }
    .numero-azul {
        background:#2471A3;
        color:white;
        text-align:center;
        padding:10px;
        border-radius:10px;
        font-size:16px;
        box-shadow:0 3px 6px rgba(0,0,0,0.15);
        margin-bottom:4px;
    }
    .bloco-jogo {
        margin-bottom:16px;
        padding-bottom:8px;
        border-bottom:1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- ESTRATÉGIAS ----------------
ESTRATEGIAS = {
    "nucleo": {
        "label": "🟢 Núcleo Inteligente™",
        "descricao": "Estratégia analítica adaptativa baseada em desempenho."
    },
    "matriz": {
        "label": "🔵 Matriz de Cobertura™",
        "descricao": "Estratégia clássica de fechamento matricial."
    }
}

# ---------------- ESTADO ----------------
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("analise_pronta", False)
st.session_state.setdefault("resultado_sim", None)
st.session_state.setdefault("estrategia", "nucleo")

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

    fechamento_nome = st.selectbox(
        "Fechamento", list(FECHAMENTOS.keys())
    )

    estrategia_sb = st.selectbox(
        "🧠 Estratégia",
        list(ESTRATEGIAS.keys()),
        index=list(ESTRATEGIAS.keys()).index(st.session_state.estrategia),
        format_func=lambda k: ESTRATEGIAS[k]["label"]
    )

    if estrategia_sb != st.session_state.estrategia:
        st.session_state.estrategia = estrategia_sb
        st.session_state.analise_pronta = False
        st.session_state.pop("melhor", None)

    st.info(ESTRATEGIAS[st.session_state.estrategia]["descricao"])
    st.write(f"👤 **{st.session_state.usuario}**")

# ---------------- APP ----------------
st.title("🍀 Núcleo 21")

# -------- SELETOR MOBILE --------
st.subheader("🧠 Estratégia de Jogo")

estrategia_mobile = st.radio(
    "Escolha a estratégia",
    options=list(ESTRATEGIAS.keys()),
    index=list(ESTRATEGIAS.keys()).index(st.session_state.estrategia),
    format_func=lambda k: ESTRATEGIAS[k]["label"],
    horizontal=True
)

if estrategia_mobile != st.session_state.estrategia:
    st.session_state.estrategia = estrategia_mobile
    st.session_state.analise_pronta = False
    st.session_state.pop("melhor", None)

st.warning(
    "⚠️ Sistema educacional e estatístico. "
    "Não prevê resultados nem garante prêmios."
)

resultado_txt = st.text_input(
    "Resultado do sorteio (6 dezenas)",
    placeholder="01 02 03 04 05 06"
)

# ---------------- ANÁLISE ----------------
if st.button("🔍 Analisar"):
    resultado = converter_lista(resultado_txt)
    if len(resultado) != 6:
        st.error("Digite exatamente 6 dezenas")
        st.stop()

    pool = list(range(1, 61))
    fechamento = FECHAMENTOS[fechamento_nome]

    if st.session_state.estrategia == "nucleo":
        _, melhor = processar_fechamento(pool, resultado, fechamento)

        registrar_analise(
            st.session_state.usuario,
            fechamento_nome,
            resultado,
            melhor["pontos"],
            melhor["numeros"],
            "nucleo"
        )

        st.session_state.melhor = melhor
        st.session_state.jogos = gerar_jogos(melhor["numeros"])
    else:
        import random
        nums = list(range(1, 61))
        random.shuffle(nums)
        st.session_state.jogos = [
            sorted(nums[i:i+6]) for i in range(0, 60, 6)
        ]

    st.session_state.analise_pronta = True
    st.session_state.resultado_sim = None

# ---------------- RESULTADOS ----------------
if st.session_state.analise_pronta:
    st.subheader("🎯 Resultado da Estratégia")

    if st.session_state.estrategia == "nucleo" and "melhor" in st.session_state:
        cols = st.columns(6)
        for c, n in zip(cols, sorted(st.session_state.melhor["numeros"])):
            c.markdown(
                f"<div class='numero-verde'>{n:02d}</div>",
                unsafe_allow_html=True
            )

    st.subheader("🎲 Jogos Gerados")

    for i, jogo in enumerate(st.session_state.jogos, 1):
        with st.container():
            st.markdown(f"**Jogo {i}**")
            cols = st.columns(6)
            for c, n in zip(cols, jogo):
                c.markdown(
                    f"<div class='numero-azul'>{n:02d}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

    # ---------------- SIMULAÇÃO ----------------
    st.subheader("🧪 Simulação Estatística")

    TOTAL_SORTEIOS = 500

    if st.button("▶️ Simular Estratégia"):
        st.session_state.resultado_sim = simular_cenario(
            st.session_state.jogos, TOTAL_SORTEIOS
        )

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média", r.get("media", 0))
        c2.metric("🏆 Máximo", r.get("maximo", 0))
        c3.metric("❌ Zeros", r.get("zeros", 0))
        c4.metric("🔢 Sorteios", TOTAL_SORTEIOS)

# ---------------- RANKING ----------------
st.divider()
st.subheader("🏅 Ranking Geral")

ranking = gerar_ranking()
if ranking:
    df = pd.DataFrame(ranking).sort_values("media", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Ainda não há dados suficientes.")

# ---------------- RODAPÉ ----------------
st.markdown(
    "<hr><div style='text-align:center;color:#777;font-size:13px;'>"
    "<strong>⚠️ Aviso Legal</strong><br>"
    "Ferramenta educacional e estatística."
    "</div>",
    unsafe_allow_html=True
)
