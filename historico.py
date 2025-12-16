import json
import os
from datetime import datetime

ARQUIVO = "historico.json"

# ===================================================
# 📂 CONTROLE DE ARQUIVO
# ===================================================

def _carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# ===================================================
# 📝 REGISTRO DE ANÁLISE
# ===================================================

def registrar_analise(
    usuario,
    fechamento,
    resultado,
    pontos,
    numeros,
    estrategia=None
):
    """
    Registra uma análise no histórico.
    'estrategia' é FUNDAMENTAL para gráficos comparativos.
    """

    dados = _carregar()

    dados.append({
        "usuario": usuario,
        "fechamento": fechamento,
        "resultado": resultado,
        "pontos": int(pontos),
        "numeros": numeros,
        "estrategia": estrategia,  # nucleo | matriz | nucleo25
        "data": datetime.now().isoformat()
    })

    _salvar(dados)


# ===================================================
# 🔧 UTILITÁRIOS
# ===================================================

def _extrair_pontos(d):
    p = d.get("pontos")
    if isinstance(p, (int, float)):
        return int(p)
    return None


# ===================================================
# 🏅 RANKING GERAL (POR USUÁRIO)
# ===================================================

def gerar_ranking():
    dados = _carregar()
    ranking = {}

    for d in dados:
        usuario = d.get("usuario")
        pontos = _extrair_pontos(d)

        if not usuario or pontos is None:
            continue

        ranking.setdefault(usuario, []).append(pontos)

    resultado = []
    for usuario, pts in ranking.items():
        if not pts:
            continue

        resultado.append({
            "usuario": usuario,
            "media": round(sum(pts) / len(pts), 2),
            "analises": len(pts),
            "maximo": max(pts)
        })

    return resultado


# ===================================================
# 🧑‍💻 RANKING INDIVIDUAL
# ===================================================

def gerar_ranking_por_usuario(usuario):
    dados = _carregar()
    pts = []

    for d in dados:
        if d.get("usuario") != usuario:
            continue

        pontos = _extrair_pontos(d)
        if pontos is not None:
            pts.append(pontos)

    if not pts:
        return []

    return [{
        "usuario": usuario,
        "media": round(sum(pts) / len(pts), 2),
        "analises": len(pts),
        "maximo": max(pts)
    }]


# ===================================================
# 📜 HISTÓRICO COMPLETO DO USUÁRIO
# ===================================================

def listar_analises_usuario(usuario):
    dados = _carregar()

    registros = [
        d for d in dados
        if d.get("usuario") == usuario
    ]

    registros.sort(key=lambda x: x.get("data", ""))
    return registros


# ===================================================
# 📈 RESUMO POR ESTRATÉGIA (GRÁFICO)
# ===================================================

def resumo_por_estrategia(usuario):
    """
    Retorna desempenho médio por estratégia:
    - nucleo
    - matriz
    - nucleo25
    """

    dados = _carregar()
    mapa = {}

    for d in dados:
        if d.get("usuario") != usuario:
            continue

        estrategia = d.get("estrategia")
        pontos = _extrair_pontos(d)

        if not estrategia or pontos is None:
            continue

        mapa.setdefault(estrategia, []).append(pontos)

    resultado = []
    for estrategia, pts in mapa.items():
        if not pts:
            continue

        resultado.append({
            "estrategia": estrategia,
            "media": round(sum(pts) / len(pts), 2),
            "analises": len(pts),
            "maximo": max(pts)
        })

    return resultado
