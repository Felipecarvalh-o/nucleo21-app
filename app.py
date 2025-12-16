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

# ================= ESTILO GLOBAL =================
st.markdown("""
<style>
.botao-estrategia button {
    width:100%;
    height:60px;
    font-size:16px;
    font-weight:700;
    border-radius:14px;
}
.numero-verde {background:#1E8449;color:white;padding:12px;border-radius:12px;font-size:20px;font-weight:700;text-align:center;}
.numero-azul {background:#2471A3;color:white;padding:10px;border-radius:10px;font-size:16px;text-align:center;}
.numero-roxo {background:#8E44AD;color:white;padding:10px;border-radius:10px;font-size:16px;text-align:center;}
.bloco-jogo {margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e0e0e0;}
</style>
""", unsafe_allow_html=True)

# ================= ESTRATÉGIAS =================
ESTRATEGIAS = {
    "nucleo": {
        "label": "🟢 Núcleo Inteligente™",
        "descricao": (
            "Analisa o fechamento escolhido, identifica a linha com melhor "
            "desempenho frente ao resultado informado e gera jogos otimizados "
            "a partir desse núcleo."
        )
    },
    "matriz": {
        "label": "🔵 Matriz de Cobertura™",
        "descricao": (
            "Geração clássica e aleatória de jogos, focada em cobertura ampla "
            "e simplicidade operacional."
        )
    },
    "nucleo25": {
        "label": "🟣 Núcleo Expandido 25™",
        "descricao": (
            "Selecione exatamente 25 dezenas estratégicas. O sistema gera "
            "automaticamente 190 jogos organizados, com alta distribuição "
            "combinatória e foco educacional."
        )
    }
}

# ================= ESTADO =================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("estrategia", "nucleo")
st.session_state.setdefault("analise_pronta", False)
st.session_state.setdefault("resultado_sim", None)

# ================= LOGIN =================
if not st.session_state.logado:
    st.title("🔐 Acesso ao Núcleo 21")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar") and u and s:
        st.session_state.logado = True
        st.session_state.usuario = u
        st.rerun()
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚙️ Configurações")
    fechamento_nome = st.selectbox("Fechamento", list(FECHAMENTOS.keys()))
    st.write(f"👤 **{st.session_state.usuario}**")

# ================= MENU SUPERIOR =================
st.title("🍀 Núcleo 21")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🟢 Núcleo Inteligente™", use_container_width=True):
        st.session_state.estrategia = "nucleo"
        st.session_state.analise_pronta = False
with c2:
    if st.button("🔵 Matriz de Cobertura™", use_container_width=True):
        st.session_state.estrategia = "matriz"
        st.session_state.analise_pronta = False
with c3:
    if st.button("🟣 Núcleo Expandido 25™", use_container_width=True):
        st.session_state.estrategia = "nucleo25"
        st.session_state.analise_pronta = False

# ================= DESCRIÇÃO =================
st.info(ESTRATEGIAS[st.session_state.estrategia]["descricao"])

# ================= INPUTS =================
if st.session_state.estrategia == "nucleo25":
    dezenas_txt = st.text_area("Digite as 25 dezenas", placeholder="01 02 03 ... 25")
else:
    resultado_txt = st.text_input("Resultado do sorteio (6 dezenas)")

# ================= ANÁLISE =================
if st.button("🔍 Analisar"):

    if st.session_state.estrategia == "nucleo25":
        dezenas = converter_lista(dezenas_txt)
        st.session_state.jogos = gerar_jogos_nucleo25(dezenas)
        st.session_state.analise_pronta = True

    else:
        resultado = converter_lista(resultado_txt)
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
            st.session_state.jogos = [sorted(nums[i:i+6]) for i in range(0, 60, 6)]

        st.session_state.analise_pronta = True

# ================= RESULTADOS =================
if st.session_state.analise_pronta:
    st.subheader("🎲 Jogos Gerados")
    for i, jogo in enumerate(st.session_state.jogos, 1):
        st.markdown(f"**Jogo {i}**")
        cols = st.columns(6)
        for c, n in zip(cols, jogo):
            cor = "numero-roxo" if st.session_state.estrategia == "nucleo25" else "numero-azul"
            c.markdown(f"<div class='{cor}'>{n:02d}</div>", unsafe_allow_html=True)
        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

# ================= GRÁFICO =================
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

# ================= RANKING =================
st.divider()
st.subheader("🏅 Ranking Geral")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)
