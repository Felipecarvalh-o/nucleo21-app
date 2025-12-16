import streamlit as st
import pandas as pd
import plotly.express as px

from engine import processar_fechamento, gerar_jogos
from historico import registrar_analise, gerar_ranking, listar_analises_usuario
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
        margin-bottom:4px;
    }
    .numero-azul {
        background:#2471A3;
        color:white;
        text-align:center;
        padding:10px;
        border-radius:10px;
        font-size:16px;
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
        "descricao": "Seleciona a melhor linha do fechamento com base em desempenho."
    },
    "matriz": {
        "label": "🔵 Matriz de Cobertura™",
        "descricao": "Geração clássica de jogos com foco em cobertura matemática."
    },
   "nucleo25": {
    "label": "🟣 Núcleo 25™",
    "descricao": (
        "Estratégia avançada baseada em um núcleo ampliado de 25 dezenas. "
        "Organiza combinações de forma estruturada para maximizar cobertura "
        "e consistência estatística dentro de um conjunto expandido."
    )
}

# ---------------- ESTADO ----------------
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("estrategia", "nucleo")
st.session_state.setdefault("analise_pronta", False)
st.session_state.setdefault("resultado_sim", None)

# ---------------- LOGIN ----------------
if not st.session_state.logado:
    st.title("🔐 Acesso ao Núcleo 21")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar") and u and s:
        st.session_state.logado = True
        st.session_state.usuario = u
        st.rerun()
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    fechamento_nome = st.selectbox("Fechamento", list(FECHAMENTOS.keys()))

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

# ---------------- APP ----------------
st.title("🍀 Núcleo 21")

# -------- SELETOR MOBILE --------
estrategia_mobile = st.radio(
    "🧠 Estratégia de Jogo",
    options=list(ESTRATEGIAS.keys()),
    index=list(ESTRATEGIAS.keys()).index(st.session_state.estrategia),
    format_func=lambda k: ESTRATEGIAS[k]["label"],
    horizontal=True
)

if estrategia_mobile != st.session_state.estrategia:
    st.session_state.estrategia = estrategia_mobile
    st.session_state.analise_pronta = False
    st.session_state.pop("melhor", None)

resultado_txt = st.text_input("Resultado do sorteio (6 dezenas)")

# ---------------- ANÁLISE ----------------
if st.button("🔍 Analisar"):

    # -------- FECHAMENTO 25 (stub) --------
    if st.session_state.estrategia == "fechamento25":
        st.warning(
            "🟣 **Fechamento Garantido 25™** está em implementação.\n\n"
            "Na próxima etapa você poderá selecionar 25 dezenas "
            "e gerar automaticamente 190 jogos com garantia matemática."
        )
        st.stop()

    # -------- ESTRATÉGIAS EXISTENTES --------
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

    elif st.session_state.estrategia == "matriz":
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
    if st.session_state.estrategia == "nucleo" and "melhor" in st.session_state:
        cols = st.columns(6)
        for c, n in zip(cols, st.session_state.melhor["numeros"]):
            c.markdown(
                f"<div class='numero-verde'>{n:02d}</div>",
                unsafe_allow_html=True
            )

    st.subheader("🎲 Jogos Gerados")
    for i, jogo in enumerate(st.session_state.jogos, 1):
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
    TOTAL = 500

    if st.button("▶️ Simular Estratégia"):
        st.session_state.resultado_sim = simular_cenario(
            st.session_state.jogos, TOTAL
        )

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Máximo", r["maximo"])
        c3.metric("❌ Zeros", r["zeros"])
        c4.metric("🔢 Sorteios", TOTAL)

# ---------------- GRÁFICO ESTRATÉGIAS ----------------
st.divider()
st.subheader("📈 Comparativo das Estratégias")

dados = listar_analises_usuario(st.session_state.usuario)
if dados:
    df = pd.DataFrame(dados)
    if "estrategia" in df.columns:
        fig = px.line(
            df,
            x=df.index,
            y="pontos",
            color="estrategia",
            markers=True,
            color_discrete_map={
                "nucleo": "#1E8449",
                "matriz": "#2471A3",
                "fechamento25": "#8E44AD"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- RANKING ----------------
st.divider()
st.subheader("🏅 Ranking Geral")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)

