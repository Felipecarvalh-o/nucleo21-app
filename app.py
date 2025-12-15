import streamlit as st
from utils import converter_lista, validar_pool
from fechamentos import FECHAMENTOS
from engine import analisar_e_salvar
from historico import carregar_historico, ranking_jogos

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
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

h1 {
    font-weight: 800;
    letter-spacing: -0.03em;
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
    font-size: 1rem;
    border: none;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #16a34a, #15803d);
}

details {
    background: #020617;
    border-radius: 14px;
    padding: 1rem;
    border: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO ----------------
st.title("🍀 Núcleo 21")
st.caption("Analisador estatístico baseado em combinações e fechamentos reduzidos")

# ---------------- AVISO LEGAL ----------------
with st.expander("⚠️ Aviso Importante", expanded=False):
    st.write("""
    Este aplicativo é uma ferramenta de **análise estatística e matemática**.

    • Não garante prêmios  
    • Não aumenta probabilidades oficiais  
    • Não possui vínculo com a Caixa Econômica Federal  

    Resultados apresentados são apenas simulações baseadas em combinações.
    Utilize este sistema exclusivamente para fins **educacionais e de entretenimento**.
    Jogue com responsabilidade.
    """)

st.divider()

# ---------------- INPUTS ----------------
pool_text = st.text_area(
    "1️⃣ Base de 60 dezenas (ou deixe vazio para usar 01–60)",
    height=110
)

resultado_text = st.text_input(
    "2️⃣ Resultado do sorteio (6 dezenas)"
)

fechamento_nome = st.selectbox(
    "3️⃣ Modelo de Análise",
    list(FECHAMENTOS.keys())
)

# ---------------- PROCESSAMENTO ----------------
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

    linhas, melhor, jogos = analisar_e_salvar(
        pool,
        resultado,
        FECHAMENTOS[fechamento_nome],
        fechamento_nome
    )

    st.divider()
    st.subheader("📊 Resultado da Análise")

    for l in linhas:
        cor = "🟢" if l["pontos"] >= 4 else "🟡" if l["pontos"] == 3 else "🔴"
        st.write(
            f"{cor} **Linha {l['linha']}** — "
            f"{l['pontos']} pontos | "
            f"Números: {sorted(l['numeros'])}"
        )

    st.divider()
    st.success(
        f"🏆 Destaque Estatístico: **Linha {melhor['linha']}** "
        f"com **{melhor['pontos']} pontos**"
    )

    st.subheader("🎯 Combinações Geradas (6 dezenas)")
    for i, jogo in enumerate(jogos, 1):
        st.write(f"🎟️ Jogo {i}: {jogo}")

# ---------------- HISTÓRICO ----------------
st.divider()
st.subheader("📚 Histórico de Análises")

historico = carregar_historico()

if historico:
    for h in historico[-5:][::-1]:
        st.write(
            f"🕒 {h['data']} | "
            f"Fechamento: {h['fechamento']} | "
            f"Melhor Linha: {h['melhor_linha']} | "
            f"Pontos: {h['pontos']}"
        )
else:
    st.info("Nenhuma análise registrada ainda.")

# ---------------- RANKING ----------------
st.divider()
st.subheader("🏆 Ranking Estatístico de Jogos")

ranking = ranking_jogos()

if ranking:
    for i, (jogo, media, vezes) in enumerate(ranking[:5], 1):
        st.write(
            f"{i}️⃣ 🎟️ {jogo} — "
            f"Média: **{media:.2f} pontos** | "
            f"Aparições: {vezes}"
        )
else:
    st.info("Ranking será exibido após mais análises.")
