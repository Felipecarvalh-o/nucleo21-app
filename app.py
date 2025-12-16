import streamlit as st
import pandas as pd
import plotly.express as px

from engine import (
    processar_fechamento,
    gerar_jogos,
    gerar_jogos_nucleo25
)
from historico import registrar_analise, gerar_ranking, listar_analises_usuario
from utils import converter_lista
from fechamentos import FECHAMENTOS
from simulador import simular_cenario

st.set_page_config("Núcleo 21", "🍀", layout="centered")

# ================= ESTILO GLOBAL =================
st.markdown("""
<style>
.numero-verde {background:#1E8449;color:white;padding:12px;border-radius:12px;font-size:20px;font-weight:700;text-align:center;}
.numero-azul {background:#2471A3;color:white;padding:10px;border-radius:10px;font-size:16px;text-align:center;}
.numero-roxo {background:#8E44AD;color:white;padding:10px;border-radius:10px;font-size:16px;text-align:center;}
.bloco-jogo {margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #e0e0e0;}
.descricao {font-size:15px;line-height:1.6;}
.aviso {font-size:12px;color:#777;margin-top:6px;}
.score {font-size:14px;font-weight:600;margin-top:8px;}
</style>
""", unsafe_allow_html=True)

# ================= ONBOARDING =================
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 1

if st.session_state.onboarding_step <= 3:
    st.title("🍀 Bem-vindo ao Núcleo 21")

    mensagens = {
        1: "Aqui você organiza jogos com base em critérios estatísticos e históricos.",
        2: "As estratégias ajudam a estruturar cenários, não prever resultados.",
        3: "Escolha uma estratégia, analise e explore os comportamentos possíveis."
    }

    st.info(mensagens[st.session_state.onboarding_step])

    if st.button("➡️ Próximo"):
        st.session_state.onboarding_step += 1

    st.stop()

# ================= ESTRATÉGIAS =================
ESTRATEGIAS = {
    "nucleo": {
        "titulo": "🍀 Núcleo Inteligente™",
        "cor": "#1E8449",
        "score": "🟢 Organização Alta",
        "descricao": "Leitura focada em desempenho histórico e eficiência observada."
    },
    "matriz": {
        "titulo": "🍀 Matriz de Cobertura™",
        "cor": "#2471A3",
        "score": "🔵 Distribuição Equilibrada",
        "descricao": "Amplitude estratégica e presença estatística organizada."
    },
    "nucleo25": {
        "titulo": "🍀 Núcleo Expandido 25™",
        "cor": "#8E44AD",
        "score": "🟣 Estrutura Avançada",
        "descricao": "Alta massa crítica com controle e disciplina estatística."
    }
}

# ================= ESTADO =================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("estrategia", "nucleo")
st.session_state.setdefault("analise_pronta", False)
st.session_state.setdefault("resultado_sim", None)

# ================= LOGIN =================
if not st.session_state.logado:
    st.title("🔐 Acesso ao Núcleo 21")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("🔐 Acessar Painel de Estratégias") and u and s:
        st.session_state.logado = True
        st.session_state.usuario = u
        st.rerun()
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    fechamento_nome = st.selectbox("🎯 Fechamento Utilizado", list(FECHAMENTOS.keys()))

    with st.expander("📘 Como funciona a simulação"):
        st.write("""
        A simulação executa sorteios aleatórios independentes
        e observa o comportamento dos jogos nesses cenários.

        Ela **não prevê resultados futuros**
        e **não garante desempenho real**.
        """)

# ================= TOPO =================
st.title("🍀 Núcleo 21")

c1, c2, c3 = st.columns(3)
if c1.button("🍀 Ativar Leitura Inteligente", use_container_width=True):
    st.session_state.estrategia = "nucleo"
if c2.button("🍀 Ativar Cobertura Estratégica", use_container_width=True):
    st.session_state.estrategia = "matriz"
if c3.button("🍀 Ativar Núcleo Avançado", use_container_width=True):
    st.session_state.estrategia = "nucleo25"

estr = ESTRATEGIAS[st.session_state.estrategia]

st.markdown(
    f"""
    <div style="border-left:6px solid {estr['cor']}; padding-left:12px;">
        <h4 style="color:{estr['cor']};">{estr['titulo']}</h4>
        <div class="descricao">{estr['descricao']}</div>
        <div class="score">{estr['score']}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div class='aviso'>Uso estatístico e histórico. Não há garantia de premiação.</div>",
    unsafe_allow_html=True
)

# ================= INPUT =================
if st.session_state.estrategia == "nucleo25":
    dezenas_txt = st.text_area("🧩 Selecione as 25 dezenas que formarão o núcleo")
else:
    resultado_txt = st.text_input("🎯 Informe as dezenas sorteadas para análise")

# ================= PROCESSAMENTO =================
if st.button("🔍 Executar Leitura Estratégica"):

    if st.session_state.estrategia == "nucleo25":
        st.session_state.jogos = gerar_jogos_nucleo25(
            converter_lista(dezenas_txt)
        )
    else:
        resultado = converter_lista(resultado_txt)
        pool = list(range(1, 61))
        fechamento = FECHAMENTOS[fechamento_nome]

        if st.session_state.estrategia == "nucleo":
            _, destaque = processar_fechamento(pool, resultado, fechamento)
            registrar_analise(
                st.session_state.usuario,
                fechamento_nome,
                resultado,
                destaque["pontos"],
                destaque["numeros"],
                "nucleo"
            )
            st.session_state.jogos = gerar_jogos(destaque["numeros"])
        else:
            import random
            nums = list(range(1, 61))
            random.shuffle(nums)
            st.session_state.jogos = [
                sorted(nums[i:i+6]) for i in range(0, 60, 6)
            ]

    st.session_state.analise_pronta = True
    st.session_state.resultado_sim = None

# ================= RESULTADOS =================
if st.session_state.analise_pronta:

    st.subheader("🎲 Jogos Organizados pela Estratégia")
    for jogo in st.session_state.jogos:
        cols = st.columns(6)
        for c, n in zip(cols, jogo):
            css = (
                "numero-verde" if st.session_state.estrategia == "nucleo"
                else "numero-roxo" if st.session_state.estrategia == "nucleo25"
                else "numero-azul"
            )
            c.markdown(f"<div class='{css}'>{n:02d}</div>", unsafe_allow_html=True)

    st.subheader("🧪 Simulação de Cenários Possíveis")
    if st.button("▶️ Testar Comportamento da Estratégia"):
        st.session_state.resultado_sim = simular_cenario(st.session_state.jogos)

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média de Desempenho", r["media"],
                  help="Média do melhor desempenho observado nos cenários.")
        c2.metric("🏆 Melhor Cenário", r["maximo"],
                  help="Maior pontuação observada em um cenário.")
        c3.metric("❌ Cenários sem Pontuação", r["zeros"],
                  help="Quantidade de cenários sem acertos.")
        c4.metric("🔢 Amostras Simuladas", r["total"])

# ================= GRÁFICO =================
st.divider()
st.subheader("📈 Evolução de Desempenho por Estratégia")

dados = listar_analises_usuario(st.session_state.usuario)
if dados:
    df = pd.DataFrame(dados)
    fig = px.line(
        df,
        x=df.index,
        y="pontos",
        color="estrategia",
        markers=True,
        color_discrete_map={
            "nucleo": "#1E8449",
            "matriz": "#2471A3",
            "nucleo25": "#8E44AD"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= RANKING =================
st.divider()
st.subheader("🏅 Ranking de Consistência Estratégica")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)
