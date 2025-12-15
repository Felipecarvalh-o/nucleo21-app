import json
import os
from datetime import datetime

ARQUIVO = "historico.json"

def _carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def registrar_analise(usuario, fechamento, resultado, pontos, numeros):
    dados = _carregar()
    dados.append({
        "usuario": usuario,
        "fechamento": fechamento,
        "resultado": resultado,
        "pontos": int(pontos),  # garante tipo correto
        "numeros": numeros,
        "data": datetime.now().isoformat()
    })
    _salvar(dados)

def _extrair_pontos(d):
    """
    Extrai apenas pontuação válida (int ou float).
    Ignora listas, strings ou valores inválidos.
    """
    p = d.get("pontos")

    if isinstance(p, (int, float)):
        return p

    return None

def gerar_ranking():
    dados = _carregar()
    ranking = {}

    for d in dados:
        u = d.get("usuario")
        pontos = _extrair_pontos(d)

        if u is None or pontos is None:
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

def listar_analises_usuario(usuario):
    dados = _carregar()
    registros = [
        d for d in dados if d.get("usuario") == usuario
    ]
    registros.sort(key=lambda x: x.get("data", ""))
    return registros
