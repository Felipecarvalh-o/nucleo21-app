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
.numero-verde {background:#1E8449;color:white;padding:12px;border-radius:12px;font-size:20px;font-weight:700;text-align:center;}
.numero-azul {background:#2471A3;color:white;padding:10px;border-radius:10px;font-size:16px;text-align:center;}
.numero-roxo {background:#8E44AD;color:white;padding:10px;border-radius:10px;font-size:16px;text-align:center;}
.bloco-jogo {margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e0e0e0;}
.descricao {font-size:15px;line-height:1.5;}
.aviso {font-size:12px;color:#777;}
</style>
""", unsafe_allow_html=True)

# ================= ESTRATÉGIAS =================
ESTRATEGIAS = {
    "nucleo": {
        "label": "🍀 Núcleo Inteligente™",
        "cor": "#1E8449",
        "descricao": """
        <div class='descricao'>
        Onde muitos veem dezenas, o <b>Núcleo Inteligente™</b> enxerga padrões.<br>
        Analisa o desempenho histórico do fechamento e destaca a linha mais eficiente,
        seguindo a lógica do <i>“jogar no miolo”</i>, muito citada por apostadores experientes.
        </div>
        """
    },
    "matriz": {
        "label": "🍀 Matriz de Cobertura™",
        "cor": "#2471A3",
        "descricao": """
        <div class='descricao'>
        Estratégia focada em <b>amplitude e equilíbrio</b>.<br>
        Distribui as dezenas de forma organizada para ampliar a presença estatística
        nos sorteios, respeitando a lógica matemática dos fechamentos.
        </div>
        """
    },
    "nucleo25": {
        "label": "🍀 Núcleo Expandido 25™",
        "cor": "#8E44AD",
        "descricao": """
        <div class='descricao'>
        Para quem gosta de trabalhar com <b>mais massa crítica</b>.<br>
        Expande o núcleo principal para até 25 dezenas,
        mantendo organização, leitura estatística e disciplina de jogo —
        abordagem comum entre quem estuda ciclos e repetição de padrões.
        </div>
        """
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
    fechamento_nome = st.selectbox("Fechamento", list(FECHAMENTOS.keys()))
    st.write(f"👤 **{st.session_state.usuario}**")

# ================= MENU SUPERIOR =================
st.title("🍀 Núcleo 21")

c1, c2, c3 = st.columns(3)
if c1.button("🍀 Núcleo Inteligente™", use_container_width=True):
    st.session_state.estrategia = "nucleo"
    st.session_state.analise_pronta = False

if c2.button("🍀 Matriz de Cobertura™", use_container_width=True):
    st.session_state.estrategia = "matriz"
    st.session_state.analise_pronta = False

if c3.button("🍀 Núcleo Expandido 25™", use_container_width=True):
    st.session_state.estrategia = "nucleo25"
    st.session_state.analise_pronta = False

st.markdown(ESTRATEGIAS[st.session_state.estrategia]["descricao"], unsafe_allow_html=True)

st.markdown("""
<div class='aviso'>
As estratégias utilizam critérios estatísticos e históricos.
A Mega-Sena é um jogo de azar e não há garantia de premiação.
</div>
""", unsafe_allow_html=True)

# ================= INPUTS =================
if st.session_state.estrategia == "nucleo25":
    dezenas_txt = st.text_area("Digite as 25 dezenas")
else:
    resultado_txt = st.text_input("Resultado do sorteio (6 dezenas)")

# ================= ANÁLISE =================
if st.button("🔍 Analisar"):

    if st.session_state.estrategia == "nucleo25":
        dezenas = converter_lista(dezenas_txt)
        st.session_state.jogos = gerar_jogos_nucleo25(dezenas)

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
            st.session_state.jogos = gerar_jogos(melhor["numeros"])

        else:
            import random
            nums = list(range(1, 61))
            random.shuffle(nums)
            st.session_state.jogos = [sorted(nums[i:i+6]) for i in range(0, 60, 6)]

    st.session_state.analise_pronta = True
    st.session_state.resultado_sim = None

# ================= RESULTADOS =================
if st.session_state.analise_pronta:

    st.subheader("🎲 Jogos Gerados")
    for jogo in st.session_state.jogos:
        cols = st.columns(6)
        for c, n in zip(cols, jogo):
            css = (
                "numero-verde" if st.session_state.estrategia == "nucleo"
                else "numero-roxo" if st.session_state.estrategia == "nucleo25"
                else "numero-azul"
            )
            c.markdown(f"<div class='{css}'>{n:02d}</div>", unsafe_allow_html=True)
        st.markdown("<div class='bloco-jogo'></div>", unsafe_allow_html=True)

    # ================= SIMULAÇÃO =================
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
