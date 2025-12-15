import streamlit as st
from engine import (
    processar_fechamento,
    gerar_jogos,
    carregar_historico
)

st.set_page_config(
    page_title="Núcleo 21",
    page_icon="🍀",
    layout="centered"
)

st.title("🍀 Núcleo 21")
st.caption("Análise estatística educacional · Sem promessas de ganho")

st.warning(
    "Esta ferramenta é apenas educacional e estatística. "
    "Não garante ganhos e não interfere na aleatoriedade oficial da Mega-Sena."
)

pool_text = st.text_area("Base de 60 dezenas (opcional)", placeholder="01 02 03 ... 60")
resultado_text = st.text_input("Resultado do sorteio (6 dezenas)", placeholder="05 12 18 32 41 56")

if st.button("🔍 ANALISAR AGORA", use_container_width=True):
    pool = list(range(1, 61))
    resultado = list(map(int, resultado_text.split()))

    fechamento = [
        [1,2,3,4,5,6],
        [7,8,9,10,11,12],
        [13,14,15,16,17,18],
        [19,20,21,22,23,24],
        [25,26,27,28,29,30],
        [31,32,33,34,35,36]
    ]

    linhas, melhor = processar_fechamento(pool, resultado, fechamento)

    st.subheader("🏆 Melhor Linha")
    st.success(f"{sorted(melhor['numeros'])} — {melhor['pontos']} pontos")

    st.subheader("🎟️ Sugestões de Jogos")
    for jogo in gerar_jogos(melhor["numeros"]):
        st.write(jogo)

# 🔽 HISTÓRICO 🔽
st.divider()
st.subheader("📜 Histórico de Análises")

historico = carregar_historico()

if not historico:
    st.info("Nenhuma análise registrada ainda.")
else:
    for h in reversed(historico[-10:]):
        st.write(
            f"📅 {h['data']} | "
            f"🎯 {h['pontos']} pontos | "
            f"📊 {sorted(h['melhor_linha'])}"
        )
