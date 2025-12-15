import streamlit as st
from utils import converter_lista, validar_pool
from engine import processar_fechamento, gerar_jogos, calcular_score
from historico import registrar_analise, gerar_ranking

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="NÚCLEO 21 • Mega-Sena",
    page_icon="🍀",
    layout="centered"
)

# ---------------- TEMA / CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #fafafa;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3, h4 {
    color: #f9fafb;
}
.stButton>button {
    background-color: #16a34a;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-weight: bold;
}
.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: #111827;
    color: #f9fafb;
}
.stSelectbox>div>div {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO ----------------
st.title("🍀 NÚCLEO 21")
st.caption("Análise estatística educacional • Sem promessas de ganho")

st.info(
    "⚠️ Esta ferramenta é apenas educacional e estatística. "
    "Não garante ganhos e não interfere na aleatoriedade oficial da Mega-Sena."
)

# ---------------- INPUTS ----------------
pool_text = st.text_area(
    "1️⃣ Base de 60 dezenas (opcional)",
    placeholder="Ex: 01 02 03 ... 60"
)

resultado_text = st.text_input(
    "2️⃣ Resultado do sorteio (6 dezenas)",
    placeholder="Ex: 05 12 18 32 41 56"
)

# Fechamento Núcleo 21 (fixo)
FECHAMENTO_NUCLEO_21 = [
    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22],
    [23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43],
    [24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44]
]

# ---------------- PROCESSAMENTO ----------------
if st.button("🔍 ANALISAR AGORA", use_container_width=True):

    pool = list(range(1, 61)) if not pool_text else converter_lista(pool_text)
    valido, erro = validar_pool(pool)

    if not valido:
        st.error(erro)
        st.stop()

    resultado = converter_lista(resultado_text)
    if len(resultado) < 6:
        st.error("Digite exatamente 6 dezenas no resultado.")
        st.stop()

    linhas, melhor = processar_fechamento(
        pool,
        resultado,
        FECHAMENTO_NUCLEO_21
    )

    score = calcular_score(linhas)
    jogos = gerar_jogos(melhor["numeros"])

    registrar_analise(
        resultado=resultado,
        fechamento="NÚCLEO 21",
        score=score,
        melhor_linha=melhor["linha"],
        jogos=jogos
    )

    # ---------------- RESULTADOS ----------------
    st.divider()
    st.subheader("📊 Resultado das Linhas")

    for l in linhas:
        cor = "🟢" if l["pontos"] >= 4 else "🟡" if l["pontos"] == 3 else "🔴"
        st.write(
            f"{cor} **Linha {l['linha']}** — "
            f"{l['pontos']} pontos | "
            f"Números: {sorted(l['numeros'])}"
        )

    st.success(
        f"🏆 Melhor Linha: Linha {melhor['linha']} "
        f"• Pontos: {melhor['pontos']}"
    )

    st.metric("📈 Score Geral", score)

    # ---------------- JOGOS ----------------
    st.subheader("🎟️ Sugestões de Jogo")
    for i, jogo in enumerate(jogos, 1):
        st.write(f"Jogo {i}: {jogo}")

    # ---------------- RANKING ----------------
    st.divider()
    st.subheader("🏆 Ranking de Análises")

    ranking = gerar_ranking()

    if ranking:
        for i, r in enumerate(ranking, 1):
            st.write(
                f"{i}º • {r['data']} — "
                f"Score {r['score']} | "
                f"Melhor Linha: {r['melhor_linha']}"
            )
    else:
        st.write("Nenhuma análise registrada ainda.")
