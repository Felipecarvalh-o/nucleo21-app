import json
import os
from datetime import datetime

ARQUIVO = "historico.json"


def carregar_historico():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def salvar_historico(historico):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)


def registrar_analise(resultado, pontos, melhor_linha):
    historico = carregar_historico()

    historico.append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "resultado": resultado,
        "score": pontos,
        "melhor_linha": melhor_linha
    })

    salvar_historico(historico)


def gerar_ranking(top=5):
    historico = carregar_historico()
    ordenado = sorted(historico, key=lambda x: x["score"], reverse=True)
    return ordenado[:top]
