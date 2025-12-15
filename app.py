import streamlit as st
from utils import converter_lista, validar_pool
from fechamentos import FECHAMENTOS
from engine import processar_fechamento, gerar_jogos

st.set_page_config(
    page_title="Mega Sena Analyzer",
    page_icon="🍀",
    layout="centered"
)

st.title("🍀 Mega Sena – Analisador Estratégico")
st.caption("Ferramenta estatística baseada em fechamentos reduzidos")

# INPUTS
pool_text = st.text_area(
    "1️⃣ Base de 60 dezenas (ou deixe vazio para 01–60)",
    height=100
)

resultado_text = st.text_input(
    "2️⃣ Resultado do sorteio (6 dezenas)"
)

fechamento_nome = st.selectbox(
    "3️⃣ Tipo de Fechamento",
    list(FECHAMENTOS.keys())
)

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

    st.divider()
    st.subheader("📊 Resultado das Linhas")

    for l in linhas:
        cor = "🟢" if l["pontos"] >= 4 else "🟡" if l["pontos"] == 3 else "🔴"
        st.write(
            f"{cor} **Linha {l['linha']}** — "
            f"{l['pontos']} pontos | "
            f"Números: {sorted(l['numeros'])}"
        )

    st.divider()
    st.success(
        f"🏆 Melhor Linha: **Linha {melhor['linha']}** "
        f"com **{melhor['pontos']} pontos**"
    )

    jogos = gerar_jogos(melhor["numeros"])

    st.subheader("🎯 Sugestão de Jogos (6 dezenas)")
    for i, jogo in enumerate(jogos, 1):
        st.write(f"Jogo {i}: 🎟️ {jogo}")
