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

    # =============================
    # MELHOR LINHA (BONITO)
    # =============================
    st.subheader("🏆 Melhor Linha")

    cols = st.columns(6)
    for col, n in zip(cols, sorted(melhor["numeros"])):
        col.markdown(
            f"""
            <div style="
                text-align:center;
                padding:10px;
                border-radius:8px;
                background-color:#2ecc71;
                color:white;
                font-weight:bold;
                font-size:18px;
            ">
                {str(n).zfill(2)}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(f"🎯 Pontuação: **{melhor['pontos']} pontos**")

    # =============================
    # JOGOS SUGERIDOS (FILEIRAS)
    # =============================
    st.subheader("🎟️ Sugestões de Jogos")

    for jogo in gerar_jogos(melhor["numeros"]):
        cols = st.columns(6)
        for col, n in zip(cols, jogo):
            col.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:8px;
                    border-radius:6px;
                    background-color:#f0f2f6;
                    font-weight:600;
                ">
                    {str(n).zfill(2)}
                </div>
                """,
                unsafe_allow_html=True
            )
        st.write("")

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
    st.info(
        "ℹ️ Faça pelo menos **3 análises** para identificar padrões."
    )

# =============================
# EVOLUÇÃO NO TEMPO
# =============================
st.divider()
st.subheader("📈 Sua Evolução ao Longo do Tempo")

if len(user_data) >= 3:
    df = pd.DataFrame(user_data)
    df["ordem"] = range(1, len(df) + 1)

    st.line_chart(df, x="ordem", y="score")

    tendencia = df["score"].iloc[-1] - df["score"].iloc[0]

    if tendencia > 0:
        st.success("⬆️ Tendência de melhora.")
    elif tendencia < 0:
        st.warning("⬇️ Queda recente.")
    else:
        st.info("➡️ Pontuação estável.")
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
