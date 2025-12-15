import streamlit as st
from engine import processar_fechamento, gerar_jogos
from historico import registrar_analise, carregar_historico, gerar_ranking
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
# LOGIN SIMPLES
# =============================
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔐 Acesso ao Núcleo 21")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == "admin" and senha == "123":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

    st.stop()

# =============================
# APP
# =============================
st.title("🍀 Núcleo 21")
st.caption("Análise estatística educacional · Sem promessas de ganho")

st.warning(
    "Ferramenta educacional. Não garante ganhos "
    "e não interfere na aleatoriedade oficial."
)

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.header("⚙️ Configurações")
    fechamento_nome = st.selectbox(
        "Escolha o fechamento",
        list(FECHAMENTOS.keys())
    )

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
        st.error("Informe exatamente 6 dezenas válidas.")
        st.stop()

    pool = list(range(1, 61))
    fechamento = FECHAMENTOS[fechamento_nome]

    linhas, melhor = processar_fechamento(pool, resultado, fechamento)

    registrar_analise(resultado, melhor["pontos"], melhor["numeros"])

    # =============================
    # RESULTADOS
    # =============================
    st.subheader("🏆 Melhor Linha")
    st.success(f"{sorted(melhor['numeros'])} — {melhor['pontos']} pontos")

    st.subheader("🎟️ Sugestões de Jogos")
    for jogo in gerar_jogos(melhor["numeros"]):
        st.write(jogo)

# =============================
# RANKING
# =============================
st.divider()
st.subheader("🏆 Ranking Geral")

ranking = gerar_ranking()

if not ranking:
    st.info("Nenhuma análise registrada ainda.")
else:
    for i, r in enumerate(ranking, 1):
        st.write(f"{i}º — {r['score']} pontos — {r['data']}")

# =============================
# HISTÓRICO
# =============================
st.divider()
st.subheader("📜 Histórico Recente")

historico = carregar_historico()

for h in reversed(historico[-5:]):
    st.write(
        f"📅 {h['data']} | "
        f"🎯 {h['score']} pontos | "
        f"📊 {sorted(h['melhor_linha'])}"
    )
