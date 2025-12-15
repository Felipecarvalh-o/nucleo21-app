import streamlit as st
import json
import os
from utils import converter_lista, validar_pool
from fechamentos import FECHAMENTOS
from engine import processar_fechamento, gerar_jogos, calcular_score

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Núcleo 21",
    page_icon="🍀",
    layout="centered"
)

# =========================
# CSS PREMIUM DARK (LEGÍVEL)
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #020617, #000000);
    color: #F8FAFC;
}

.block-container {
    padding-top: 3rem;
    max-width: 760px;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, span, label, div {
    color: #E5E7EB !important;
}

textarea, input, select {
    background-color: #020617 !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    color: #F8FAFC !important;
}

::placeholder {
    color: #94A3B8 !important;
}

.stButton>button {
    background: linear-gradient(135deg, #22C55E, #16A34A);
    color: #022C22 !important;
    border-radius: 16px;
    padding: 0.85rem;
    font-weight: 700;
}

.stAlert {
    background-color: #020617;
    border: 1px solid #334155;
    color: #F8FAFC;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("🍀 Núcleo 21")
st.caption("Ferramenta estatística e educacional baseada em fechamentos reduzidos")

# =========================
# HISTÓRICO
# =========================
HIST_FILE = "historico.json"

if not os.path.exists(HIST_FILE):
    with open(HIST_FILE, "w") as f:
        json.dump([], f)

with open(HIST_FILE, "r") as f:
    historico = json.load(f)

# =========================
# INPUTS
# =========================
with st.expander("🎯 Configuração da Análise", expanded=True):

    pool_text = st.text_area(
        "1️⃣ Base de 60 dezenas (opcional)",
        height=90,
        placeholder="Ex: 1 2 3 ... 60"
    )

    resultado_text = st.text_input(
        "2️⃣ Resultado do sorteio (6 dezenas)",
        placeholder="Ex: 5 8 30 31 37 45"
    )

    fechamento_nome = st.selectbox(
        "3️⃣ Tipo de fechamento",
        list(FECHAMENTOS.keys())
    )

# =========================
# PROCESSAMENTO
# =========================
if st.button("🔍 ANALISAR AGORA", use_container_width=True):

    pool = list(range(1, 61)) if not pool_text else converter_lista(pool_text)
    valido, erro = validar_pool(pool)

    if not valido:
        st.error(erro)
        st.stop()

    resultado = converter_lista(resultado_text)
    if len(resultado) < 6:
        st.error("Digite pelo menos 6 dezenas no resultado.")
        st.stop()

    linhas, melhor = processar_fechamento(
        pool,
        resultado,
        FECHAMENTOS[fechamento_nome]
    )

    score = calcular_score(linhas)

    # Salva no histórico
    historico.append({
        "fechamento": fechamento_nome,
        "melhor_linha": melhor["linha"],
        "pontos": melhor["pontos"],
        "score": score
    })

    with open(HIST_FILE, "w") as f:
        json.dump(historico, f, indent=2)

    # =========================
    # RESUMO PREMIUM
    # =========================
    st.divider()
    st.subheader("📌 Resumo da Análise")

    st.markdown(f"""
    **🏆 Melhor Linha:** Linha {melhor['linha']}  
    **🎯 Pontos:** {melhor['pontos']}  
    **📊 Score Núcleo 21:** **{score:.2f} / 10**
    """)

    # =========================
    # RESULTADO DAS LINHAS
    # =========================
    st.divider()
    st.subheader("📊 Resultado das Linhas")

    for l in linhas:
        cor = "🟢" if l["pontos"] >= 4 else "🟡" if l["pontos"] == 3 else "🔴"
        st.write(
            f"{cor} **Linha {l['linha']}** — "
            f"{l['pontos']} pontos | "
            f"Números: {sorted(l['numeros'])}"
        )

    # =========================
    # JOGOS GERADOS
    # =========================
    jogos = gerar_jogos(melhor["numeros"])

    st.divider()
    st.subheader("🎟️ Sugestões de Jogo
