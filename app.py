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
# ESTADO GLOBAL
# =============================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

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

st.warning(
    "⚠️ **AVISO IMPORTANTE**\n\n"
    "Este aplicativo possui finalidade exclusivamente educacional e estatística. "
    "Não garante ganhos, não oferece previsões e não interfere em sorteios oficiais. "
    "Jogos de loteria são baseados em aleatoriedade."
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

    # Melhor linha
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

    # Sugestões
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
    st.caption(
        "Simulação com sorteios aleatórios para fins educacionais. "
        "Não representa previsões nem garante resultados."
    )

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

        st.info(
            "🔍 Interpretação correta:\n\n"
            "• Média indica comportamento ao longo do tempo\n"
            "• Zerar faz parte da aleatoriedade\n"
            "• Pontuações altas são raras\n\n"
            "Esta simulação não prevê resultados futuros."
        )

# =============================
# AJUSTE DE ESTRATÉGIA
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
    st.info("ℹ️ Faça pelo menos 3 análises para identificar padrões.")

# =============================
# EVOLUÇÃO
# =============================
st.divider()
st.subheader("📈 Sua Evolução ao Longo do Tempo")

if len(user_data) >= 3:
    df = pd.DataFrame(user_data)
    df["ordem"] = range(1, len(df) + 1)
    st.line_chart(df, x="ordem", y="score")
else:
    st.info("ℹ️ A evolução aparece após 3 análises.")

# =============================
# RANKINGS
# =============================
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Ranking Geral")
    for i, r in enumerate(gerar_ranking(), 1):
        st.write(f"{i}º — {r['score']} pts — {r['usuario']}")

with col2:
    st.subheader("👤 Meu Ranking")
    for i, r in enumerate(
        gerar_ranking_por_usuario(st.session_state.usuario), 1
    ):
        st.write(f"{i}º — {r['score']} pts — {r['data']}")

# =============================
# RODAPÉ LEGAL
# =============================
st.markdown(
    "<hr style='margin-top:40px;'>"
    "<div style='text-align:center; font-size:14px; color:gray; line-height:1.8;'>"
    "<div style='font-size:22px;'>⚠️</div>"
    "<strong>Aviso Legal</strong><br>"
    "Este aplicativo possui finalidade exclusivamente educacional e estatística.<br>"
    "Não garante ganhos, não oferece previsões e não interfere em sorteios oficiais.<br>"
    "Jogos de loteria são baseados em aleatoriedade.<br>"
    "Utilize este sistema por sua conta e risco."
    "</div>",
    unsafe_allow_html=True
)
