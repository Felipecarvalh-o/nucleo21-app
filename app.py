import streamlit as st
import pandas as pd
import plotly.express as px

from engine import (
    processar_fechamento,
    gerar_jogos,
    gerar_jogos_nucleo25
)
from historico import registrar_analise, gerar_ranking, listar_analises_usuario
from utils import converter_lista
from fechamentos import FECHAMENTOS
from simulador import simular_cenario

st.set_page_config("Núcleo 21", "🍀", layout="centered")

# ---------------- ESTILO ----------------
st.markdown(
    """
    <style>
    .numero-verde {background:#1E8449;color:white;padding:12px;border-radius:12px;font-size:20px;font-weight:700}
    .numero-azul {background:#2471A3;color:white;padding:10px;border-radius:10px;font-size:16px}
    .numero-roxo {background:#8E44AD;color:white;padding:10px;border-radius:10px;font-size:15px}
    .bloco-jogo {margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e0e0e0}
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
        "descricao": "Jogos aleatórios com foco em cobertura estatística."
    },
    "nucleo25": {
        "label": "🟣 Núcleo Expandido 25™",
        "descricao": "Selecione 25 dezenas e gere 190 jogos balanceados."
    }
}

# ---------------- ESTADO ----------------
for k, v in {
    "logado": False,
    "usuario": "",
    "estrategia": "nucleo",
    "analise_pronta": False,
    "resultado_sim": None
}.items():
    st.session_state.setdefault(k, v)

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
        format_func=lambda k: ESTRATEGIAS[k]["label"]
    )
    st.session_state.estrategia = estrategia_sb
    st.info(ESTRATEGIAS[estrategia_sb]["descricao"])

# ---------------- APP ----------------
st.title("🍀 Núcleo 21")

# ---------------- INPUTS ----------------
if st.session_state.estrategia == "nucleo25":
    dezenas_txt = st.text_area(
        "Digite as 25 dezenas",
        placeholder="01 02 03 ... 25"
    )
else:
    resultado_txt = st.text_input("Resultado do sorteio (6 dezenas)")

# ---------------- ANALISAR ----------------
if st.button("🔍 Analisar"):

    if st.session_state.estrategia == "nucleo25":
        dezenas = converter_lista(dezenas_txt)
        jogos = gerar_jogos_nucleo25(dezenas)

        registrar_analise(
            st.session_state.usuario,
            "Núcleo 25",
            [],
            0,
            dezenas,
            "nucleo25"
        )

        st.session_state.jogos = jogos
        st.session_state.analise_pronta = True

    else:
        resultado = converter_lista(resultado_txt)
        pool = list(range(1, 61))
        fechamento = FECHAMENTOS[fechamento_nome]

        if st.session_state.estrategia == "nucleo":
            _, melhor = processar_fechamento(pool, resultado, fechamento)
            st.session_state.jogos = gerar_jogos(melhor["numeros"])
            registrar_analise(
                st.session_state.usuario,
                fechamento_nome,
                resultado,
                melhor["pontos"],
                melhor["numeros"],
                "nucleo"
            )

        else:
            import random
            nums = list(range(1, 61))
            random.shuffle(nums)
            jogos = [sorted(nums[i:i+6]) for i in range(0, 60, 6)]
            st.session_state.jogos = jogos

            registrar_analise(
                st.session_state.usuario,
                fechamento_nome,
                resultado,
                0,
                [],
                "matriz"
            )

        st.session_state.analise_pronta = True

# ---------------- RESULTADOS ----------------
if st.session_state.analise_pronta:
    st.subheader("🎲 Jogos Gerados")
    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"**Jogo {i}**")
        cols = st.columns(6)
        for c, n in zip(cols, jogo):
            cor = "numero-roxo" if st.session_state.estrategia == "nucleo25" else "numero-azul"
            c.markdown(f"<div class='{cor}'>{n:02d}</div>", unsafe_allow_html=True)
        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

# ---------------- SIMULAÇÃO ----------------
st.subheader("🧪 Simulação Estatística")
if st.button("▶️ Simular Estratégia"):
    st.session_state.resultado_sim = simular_cenario(st.session_state.jogos, 500)

if st.session_state.resultado_sim:
    r = st.session_state.resultado_sim
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Média", r["media"])
    c2.metric("🏆 Máximo", r["maximo"])
    c3.metric("❌ Zeros", r["zeros"])
    c4.metric("🔢 Sorteios", r["total"])

# ---------------- GRÁFICO ----------------
st.divider()
st.subheader("📈 Comparativo das Estratégias")

dados = listar_analises_usuario(st.session_state.usuario)
if dados:
    df = pd.DataFrame(dados)
    fig = px.line(
        df,
        x=df.index,
        y="pontos",
        color="estrategia",
        markers=True,
        color_discrete_map={
            "nucleo": "#1E8449",
            "matriz": "#2471A3",
            "nucleo25": "#8E44AD"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- RANKING ----------------
st.divider()
st.subheader("🏅 Ranking Geral")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)
