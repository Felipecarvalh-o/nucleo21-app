import streamlit as st
import pandas as pd

from engine import processar_fechamento, gerar_jogos
from historico import registrar_analise, gerar_ranking, gerar_ranking_por_usuario
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
# ESTADOS
# =============================
defaults = {
    "logado": False,
    "usuario": "",
    "aceitou_termos": False,
    "analise_pronta": False,
    "melhor": None,
    "jogos": [],
    "resultado_sim": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
# TERMOS
# =============================
if not st.session_state.aceitou_termos:
    st.title("📄 Termos de Uso")
    st.markdown(
        """
        ⚠️ **Aviso Importante**

        O Núcleo 21 é uma ferramenta **educacional e estatística**.
        Não garante ganhos, não prevê resultados e não interfere em sorteios oficiais.
        """
    )
    concordo = st.checkbox("Li e concordo com os Termos de Uso")
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
    fechamento_nome = st.selectbox("Fechamento", list(FECHAMENTOS.keys()))
    st.divider()
    st.write(f"👤 Usuário: **{st.session_state.usuario}**")

# =============================
# APP
# =============================
st.title("🍀 Núcleo 21")
st.caption("Ferramenta educacional e estatística")

resultado_text = st.text_input(
    "Resultado do sorteio (6 dezenas)",
    placeholder="01 02 03 04 05 06"
)

if st.button("🔍 ANALISAR AGORA", use_container_width=True):
    resultado = converter_lista(resultado_text)
    if len(resultado) != 6:
        st.error("Digite exatamente 6 dezenas.")
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
            f"<div style='background:#2ecc71;color:white;"
            f"text-align:center;padding:10px;border-radius:8px;"
            f"font-size:18px;font-weight:bold;'>"
            f"{str(n).zfill(2)}</div>",
            unsafe_allow_html=True
        )
    st.caption(f"🎯 Pontuação: **{melhor['pontos']} pontos**")

    st.subheader("🎟️ Sugestões de Jogos")
    for jogo in jogos:
        cols = st.columns(6)
        for col, n in zip(cols, jogo):
            col.markdown(
                f"<div style='background:#2ecc71;color:white;"
                f"text-align:center;padding:8px;border-radius:6px;"
                f"font-weight:bold;'>"
                f"{str(n).zfill(2)}</div>",
                unsafe_allow_html=True
            )
        st.write("")

    # =============================
    # SIMULAÇÃO (layout melhorado)
    # =============================
    st.divider()
    st.subheader("🧪 Simulação Educacional")

    if st.button("▶️ Simular Estratégia", use_container_width=True):
        st.session_state.resultado_sim = simular_cenario(jogos, 500)

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Máximo", r["maximo"])
        c3.metric("⭐ ≥4", r["acima_4"])
        c4.metric("❌ Zeros", r["zeros"])

    # =============================
    # RANKING GERAL (ROBUSTO)
    # =============================
    st.divider()
    st.subheader("🏆 Ranking Geral")

    rg = gerar_ranking()

    if rg:
        df = pd.DataFrame(rg)

        # normalização de nomes
        rename_map = {
            "media_pontos": "media",
            "media": "media",
            "total_analises": "analises",
            "analises": "analises",
            "max_pontos": "maximo",
            "maximo": "maximo",
        }
        df = df.rename(columns=rename_map)

        if "media" in df.columns:
            df = df.sort_values("media", ascending=False)

        df["Posição"] = range(1, len(df) + 1)
        df["Medalha"] = df["Posição"].map({1: "🥇", 2: "🥈", 3: "🥉"}).fillna("")

        def destaque(row):
            if row.get("usuario") == st.session_state.usuario:
                return ["background-color:#e8f8f5"] * len(row)
            return [""] * len(row)

        cols = [c for c in ["Medalha", "usuario", "media", "analises", "maximo"] if c in df.columns]

        st.dataframe(
            df[cols].style.apply(destaque, axis=1),
            use_container_width=True,
            hide_index=True
        )

        if "media" in df.columns:
            st.subheader("📈 Distribuição de Médias")
            st.bar_chart(df.set_index("usuario")["media"])

    else:
        st.info("Ainda não há dados suficientes para o ranking.")

# =============================
# RODAPÉ
# =============================
st.markdown(
    "<hr><div style='text-align:center;color:gray;font-size:14px;'>"
    "⚠️ Ferramenta educacional e estatística. "
    "Não garante ganhos nem previsões."
    "</div>",
    unsafe_allow_html=True
)
