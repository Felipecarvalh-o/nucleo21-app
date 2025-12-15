import json
import os
from datetime import datetime

ARQUIVO = "historico.json"

# ---------------- ARQUIVO ----------------
def _carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ---------------- REGISTRO ----------------
def registrar_analise(usuario, fechamento, resultado, pontos, numeros, estrategia=None):
    dados = _carregar()
    dados.append({
        "usuario": usuario,
        "fechamento": fechamento,
        "resultado": resultado,
        "pontos": int(pontos),
        "numeros": numeros,
        "estrategia": estrategia,  # NOVO (opcional)
        "data": datetime.now().isoformat()
    })
    _salvar(dados)

# ---------------- UTIL ----------------
def _extrair_pontos(d):
    p = d.get("pontos")
    if isinstance(p, (int, float)):
        return p
    return None

# ---------------- RANKING GERAL ----------------
def gerar_ranking():
    dados = _carregar()
    ranking = {}

    for d in dados:
        u = d.get("usuario")
        pontos = _extrair_pontos(d)

        if not u or pontos is None:
            continue

        ranking.setdefault(u, []).append(pontos)

    resultado = []
    for u, pts in ranking.items():
        if not pts:
            continue

        resultado.append({
            "usuario": u,
            "media": round(sum(pts) / len(pts), 2),
            "analises": len(pts),
            "maximo": max(pts)
        })

    return resultado

# ---------------- RANKING POR USUÁRIO ----------------
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

# ---------------- HISTÓRICO USUÁRIO ----------------
def listar_analises_usuario(usuario):
    dados = _carregar()
    registros = [d for d in dados if d.get("usuario") == usuario]
    registros.sort(key=lambda x: x.get("data", ""))
    return registros

# ===================================================
# 🚀 NOVO — COMPARATIVO POR ESTRATÉGIA (ETAPA 2)
# ===================================================

def resumo_por_estrategia(usuario):
    """
    Retorna desempenho médio por estratégia para o usuário.
    Usa apenas registros que tenham 'estrategia'.
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
    for est, pts in mapa.items():
        if not pts:
            continue

        resultado.append({
            "estrategia": est,
            "media": round(sum(pts) / len(pts), 2),
            "analises": len(pts),
            "maximo": max(pts)
        })

    return resultado
