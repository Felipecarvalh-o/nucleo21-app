import streamlit as st
import json
import os
from datetime import datetime

from utils import converter_lista, validar_pool
from fechamentos import FECHAMENTOS
from engine import processar_fechamento, gerar_jogos, calcular_score


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Núcleo 21",
    page_icon="🍀",
    layout="centered"
)

# ===============================
# ESTILO PREMIUM (LEGÍVEL)
# ===============================
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0e1117;
    color: #f0f2f6;
}
.stTextInput input, .stTextArea textarea, .stSelectbox div {
    background-color: #1c1f26;
    color: #ffffff;
}
.stButton button {
    background: linear-gradient(90deg, #1db954, #1ed760);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)


# ===============================
# TÍTULO
# ===============================
st.title("🍀 Núcleo 21")
st.caption("Ferramenta estatística e educacional baseada em fechamentos reduzidos")


# ===============================
# INPUTS
# ===============================
with st.expander("🎯 Configuração da Análise", expanded=True):

    pool_text = st.text_area(
        "1️⃣ Base de 60 dezenas (opcional)",
        placeholder="Ex: 1 2 3 ... 60",
        height=90
    )

    resultado_text = st.text_input(
        "2️⃣ Resultado do sorteio (6 dezenas)",
        placeholder="Ex: 05 18 27 33 42 59"
    )

    fechamento_nome = st.selectbox(
        "3️⃣ Tipo de fechamento",
        list(FECHAMENTOS.keys())
    )

    analisar = st.button("🔍 ANALISAR AGORA", use_container_width=True)


# ===============================
# HISTÓRICO
# ===============================
HIST_FILE = "historico.json"

def salvar_historico(registro):
    historico = []
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            historico = json.load(f)

    historico.insert(0, registro)

    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(historico[:20], f, indent=2, ensure_ascii=False)


def carregar_historico():
    if not os.path.exists(HIST_FILE):
        return []
    with open(HIST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ===============================
# PROCESSAMENTO
# ===============================
if analisar:

    pool = list(range(1, 61)) if not pool_text else converter_lista(pool_text)
    valido, erro = validar_pool(pool)

    if not valido:
        st.error(erro)
        st.stop()

    resultado = converter_lista(resultado_text)
    if len(resultado) != 6:
        st.error("Digite exatamente 6 dezenas no resultado.")
        st.stop()

    linhas, melhor = processar_fechamento(
        pool,
        resultado,
        FECHAMENTOS[fechamento_nome]
    )

    score = calcular_score(linhas)

    salvar_historico({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fechamento": fechamento_nome,
        "melhor_linha": melhor["linha"],
        "pontos": melhor["pontos"],
        "score": score
    })

    # ===============================
    # RESULTADOS
    # ===============================
    st.divider()
    st.subheader("📊 Ranking das Linhas")

    linhas_ordenadas = sorted(linhas, key=lambda x: x["pontos"], reverse=True)

    for l in linhas_ordenadas:
        cor = "🟢" if l["pontos"] >= 4 else "🟡" if l["pontos"] == 3 else "🔴"
        st.write(
            f"{cor} **Linha {l['linha']}** — "
            f"{l['pontos']} pontos | "
            f"Números: {sorted(l['numeros'])}"
        )

    st.success(
        f"🏆 Melhor Linha: **Linha {melhor['linha']}** "
        f"com **{melhor['pontos']} pontos**"
    )

    st.metric("⭐ Score Geral", f"{score} / 10")

    # ===============================
    # JOGOS SUGERIDOS
    # ===============================
    st.divider()
    st.subheader("🎟️ Sugestões de Jogos")

    jogos = gerar_jogos(melhor["numeros"])

    for i, jogo in enumerate(jogos, 1):
        st.write(f"Jogo {i}: 🎯 {jogo}")


# ===============================
# HISTÓRICO VISUAL
# ===============================
st.divider()
st.subheader("🕒 Histórico de Análises")

historico = carregar_historico()

if historico:
    for h in historico:
        st.write(
            f"📅 {h['data']} | "
            f"{h['fechamento']} | "
            f"Linha {h['melhor_linha']} | "
            f"{h['pontos']} pts | "
            f"Score {h['score']}/10"
        )
else:
    st.caption("Nenhuma análise registrada ainda.")


# ===============================
# AVISO LEGAL
# ===============================
st.divider()
st.caption(
    "⚠️ Este aplicativo é apenas educacional e estatístico. "
    "Não garante prêmios nem altera as probabilidades reais da loteria. "
    "Jogos de azar envolvem risco."
)
