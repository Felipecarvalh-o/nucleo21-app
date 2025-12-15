import streamlit as st
import json
import os
from datetime import datetime

from utils import converter_lista, validar_pool
from fechamentos import FECHAMENTOS
from engine import processar_fechamento, gerar_jogos, calcular_score

# ======================
# CONFIG VISUAL (CLARO)
# ======================
st.set_page_config(
    page_title="Núcleo 21",
    page_icon="🍀",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #f7f7f7;
    color: #1a1a1a;
}
.card {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}
.small {
    color: #555;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HISTÓRICO
# ======================
HIST_FILE = "historico.json"

def carregar_historico():
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_historico(registro):
    historico = carregar_historico()
    historico.append(registro)
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# ======================
# HEADER
# ======================
st.title("🍀 Núcleo 21")
st.caption("Analisador estatístico de fechamentos — uso recreativo")

st.markdown("""
<div class="card small">
⚠️ <b>Aviso legal:</b><br>
Esta ferramenta não garante prêmios e não possui qualquer vínculo com a Caixa Econômica Federal.
Uso exclusivamente estatístico, educacional e recreativo.
</div>
""", unsafe_allow_html=True)

# ======================
# INPUTS
# ======================
pool_text = st.text_area(
    "1️⃣ Base de dezenas (até 60 números — opcional)",
    placeholder="Ex: 1 3 5 7 ...",
    height=100
)

resultado_text = st.text_input(
    "2️⃣ Resultado do sorteio (6 dezenas)",
    placeholder="Ex: 05 08 30 31 37 45"
)

fechamento_nome = st.selectbox(
    "3️⃣ Tipo de fechamento",
    list(FECHAMENTOS.keys())
)

# ======================
# PROCESSAMENTO
# ======================
if st.button("🔍 ANALISAR", use_container_width=True):

    pool = list(range(1, 61)) if not pool_text else converter_lista(pool_text)
    valido, erro = validar_pool(pool)

    if not valido:
        st.error(erro)
        st.stop()

    resultado = converter_lista(resultado_text)
    if len(resultado) < 6:
        st.error("Informe exatamente 6 dezenas no resultado.")
        st.stop()

    linhas, melhor = processar_fechamento(
        pool,
        resultado,
        FECHAMENTOS[fechamento_nome]
    )

    score = calcular_score(linhas)

    # salva histórico
    salvar_historico({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fechamento": fechamento_nome,
        "score": score,
        "melhor_linha": melhor["linha"],
        "pontos": melhor["pontos"]
    })

    # ======================
    # RESULTADOS
    # ======================
    st.subheader("📊 Resultado das Linhas")

    for l in linhas:
        if l["pontos"] >= 4:
            cor = "🟢"
        elif l["pontos"] == 3:
            cor = "🟡"
        else:
            cor = "🔴"

        st.markdown(f"""
        <div class="card">
        {cor} <b>Linha {l["linha"]}</b><br>
        Pontos: <b>{l["pontos"]}</b><br>
        Números: {sorted(l["numeros"])}
        </div>
        """, unsafe_allow_html=True)

    st.success(
        f"🏆 Melhor Linha: Linha {melhor['linha']} com {melhor['pontos']} pontos"
    )

    # ======================
    # SCORE
    # ======================
    st.subheader("⭐ Score Geral")
    st.metric("Desempenho do fechamento", f"{score} / 10")

    # ======================
    # JOGOS
    # ======================
    jogos = gerar_jogos(melhor["numeros"])

    st.subheader("🎟️ Sugestões de Jogos")
    for i, jogo in enumerate(jogos, 1):
        st.write(f"Jogo {i}: {jogo}")

# ======================
# HISTÓRICO VISUAL
# ======================
st.divider()
st.subheader("🕘 Histórico de Análises")

historico = carregar_historico()
if not historico:
    st.info("Nenhuma análise realizada ainda.")
else:
    for h in reversed(historico[-5:]):
        st.markdown(f"""
        <div class="card small">
        📅 {h["data"]}<br>
        Fechamento: <b>{h["fechamento"]}</b><br>
        Score: <b>{h["score"]}/10</b><br>
        Melhor Linha: {h["melhor_linha"]} ({h["pontos"]} pts)
        </div>
        """, unsafe_allow_html=True)
