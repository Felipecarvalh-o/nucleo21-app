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

.descricao {font-size:15px;line-height:1.6;}
.aviso {font-size:12px;color:#777;margin-top:8px;}
.score {font-size:14px;font-weight:600;margin-top:6px;}

.jogo-container {
    padding: 14px 10px;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    margin-bottom: 20px;
}

.jogo-header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:13px;
    color:#bbb;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

# ================= ONBOARDING =================
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 1

if st.session_state.onboarding_step <= 3:
    st.title("🍀 Bem-vindo ao Núcleo 21")

    mensagens = {
        1: "Aqui você organiza jogos e dezenas do jeito que o apostador gosta: com critério.",
        2: "As estratégias ajudam a chegar perto (quadra, quina), mas não prevêem resultado.",
        3: "Escolha a estratégia, analise e estude o comportamento dos jogos."
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
        "score": "🟢 Boa leitura de jogo",
        "descricao": """
        Onde muitos jogam no escuro, o <b>Núcleo Inteligente™</b> joga com leitura.<br>
        Analisa resultados passados e destaca a linha que mais <i>chegou perto</i>
        (quadra, quina ou mais), seguindo o famoso conceito de <b>jogar no miolo</b>.
        """
    },
    "matriz": {
        "titulo": "🍀 Matriz de Cobertura™",
        "cor": "#2471A3",
        "score": "🔵 Jogo bem espalhado",
        "descricao": """
        Aqui a ideia é <b>espalhar o jogo</b>.<br>
        Muito usada por quem acredita que, com volume e constância,
        uma <i>quadra ou quina acaba aparecendo</i>.
        """
    },
    "nucleo25": {
        "titulo": "🍀 Núcleo Expandido 25™",
        "cor": "#8E44AD",
        "score": "🟣 Cobertura pesada",
        "descricao": """
        Estratégia para quem gosta de jogo mais forte.<br>
        Organização de dezenas para buscar <b>cobertura pesada</b>,
        comum entre quem estuda ciclos e repetição.
        """
    }
}

# ================= ESTADO =================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", "")
st.session_state.setdefault("estrategia", "nucleo")
st.session_state.setdefault("analise_pronta", False)
st.session_state.setdefault("resultado_sim", None)
st.session_state.setdefault("modo_compacto", False)

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

    st.session_state.modo_compacto = st.toggle(
        "🔳 Modo compacto", value=st.session_state.modo_compacto
    )

    with st.expander("📘 Como funciona a simulação"):
        st.write("""
        A simulação executa sorteios aleatórios e observa
        se os jogos chegariam perto de uma quadra, quina ou mais.

        Não prevê resultados e não garante prêmio.
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
        <h4 style="color:{estr['cor']}; margin-bottom:4px;">{estr['titulo']}</h4>
        <div class="descricao">{estr['descricao']}</div>
        <div class="score">{estr['score']}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class='aviso'>
Aplicativo independente, sem vínculo com Caixa Econômica Federal ou Loterias Caixa.
Mega-Sena é jogo de azar. Não há garantia de premiação (quadra, quina ou sena).
</div>
""", unsafe_allow_html=True)

# ================= INPUT =================
if st.session_state.estrategia == "nucleo25":
    dezenas_txt = st.text_area("🧩 Selecione as 25 dezenas")
else:
    resultado_txt = st.text_input("🎯 Informe as dezenas sorteadas")

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

    for idx, jogo in enumerate(st.session_state.jogos, 1):

        if not st.session_state.modo_compacto:
            st.markdown("<div class='jogo-container'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='jogo-header'>Jogo {idx:02d}</div>",
                unsafe_allow_html=True
            )

        cols = st.columns(6)
        for c, n in zip(cols, jogo):
            css = (
                "numero-verde" if st.session_state.estrategia == "nucleo"
                else "numero-roxo" if st.session_state.estrategia == "nucleo25"
                else "numero-azul"
            )
            c.markdown(f"<div class='{css}'>{n:02d}</div>", unsafe_allow_html=True)

        jogo_txt = " ".join(f"{n:02d}" for n in jogo)
        st.button(
            "📋 Copiar jogo",
            key=f"copy_{idx}",
            help=jogo_txt
        )

        if not st.session_state.modo_compacto:
            st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🧪 Simulação de Cenários Possíveis")
    if st.button("▶️ Testar Comportamento da Estratégia"):
        st.session_state.resultado_sim = simular_cenario(st.session_state.jogos)

    if st.session_state.resultado_sim:
        r = st.session_state.resultado_sim
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Média", r["media"])
        c2.metric("🏆 Melhor", r["maximo"])
        c3.metric("❌ Zeros", r["zeros"])
        c4.metric("🔢 Amostras", r["total"])

# ================= GRÁFICO =================
st.divider()
st.subheader("📈 Evolução de Desempenho")

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
st.subheader("🏅 Ranking Geral")
ranking = gerar_ranking()
if ranking:
    st.dataframe(pd.DataFrame(ranking), use_container_width=True)
