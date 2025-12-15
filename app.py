import streamlit as st
from utils import converter_lista, validar_pool
from fechamentos import FECHAMENTOS
from engine import analisar_e_salvar
from historico import carregar_historico, ranking_jogos, exportar_historico

st.set_page_config(
    page_title="Núcleo 21 – Analisador Estatístico",
    page_icon="🍀",
    layout="centered"
)

# ---------------- CSS PREMIUM ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}
.block-container {
    padding-top: 3rem;
    max-width: 760px;
}
textarea, input, select {
    background-color: #020617 !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b !important;
    color: #e5e7eb !important;
}
.stButton>button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: #022c22;
    border-radius: 16px;
    padding: 0.85rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.title("🍀 Núcleo 21")
st.caption("Analisador estatístico baseado em combinações e fechamentos reduzidos")

with st.expander("⚠️ Aviso Importante"):
    st.write("""
    Ferramenta estatística e educacional.
    Não garante prêmios nem aumenta probabilidades oficiais.
    Jogue com responsabilidade.
    """)

pool_text = st.text_area("1️⃣ Base de 60 dezenas (ou deixe vazio)", height=100)
resultado_text = st.text_input("2️⃣ Resultado do sorteio (6 dezenas)")
fechamento_nome = st.selectbox("3️⃣ Modelo de Análise", list(FECHAMENTOS.keys()))

if st.button("🔍 ANALISAR AGORA", use_container_width=True):

    pool = list(range(1, 61)) if not pool_text else converter_lista(pool_text)
    valido, erro = validar_pool(pool)
    if not valido:
        st.error(erro)
        st.stop()

    resultado = converter_lista(resultado_text)
    if len(resultado) < 6:
        st.error("Digite 6 dezenas.")
        st.stop()

    linhas, melhor, jogos = analisar_e_salvar(
        pool, resultado, FECHAMENTOS[fechamento_nome], fechamento_nome
    )

    st.divider()
    st.subheader("📊 Resultado da Análise")

    for l in linhas:
        st.write(f"Linha {l['linha']} — {l['pontos']} pontos")

    st.success(
        f"🏆 Destaque: Linha {melhor['linha']} com {melhor['pontos']} pontos"
    )

    st.subheader("🎯 Combinações Geradas")
    for j in jogos:
        st.write(j)

st.divider()
st.subheader("📚 Histórico")
for h in carregar_historico()[-5:][::-1]:
    st.write(f"{h['data']} | {h['fechamento']} | {h['pontos']} pontos")

st.divider()
st.subheader("🏆 Ranking Estatístico")

ranking = ranking_jogos()
for i, (jogo, media, vezes) in enumerate(ranking[:5], 1):
    st.write(f"{i}️⃣ {jogo} — média {media:.2f} | {vezes}x")

st.download_button(
    "📥 Baixar histórico (CSV)",
    exportar_historico(),
    file_name="historico_nucleo21.csv"
)
