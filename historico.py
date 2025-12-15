{
  "analises": []
}
import json
import os
from datetime import datetime

ARQUIVO_HISTORICO = "historico.json"


def carregar_historico():
    if not os.path.exists(ARQUIVO_HISTORICO):
        return []

    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def salvar_historico(dados):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def registrar_analise(resultado, fechamento, score, melhor_linha, jogos):
    historico = carregar_historico()

    registro = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "resultado": resultado,
        "fechamento": fechamento,
        "score": score,
        "melhor_linha": melhor_linha,
        "jogos": jogos
    }

    historico.append(registro)
    salvar_historico(historico)


def gerar_ranking(top=5):
    historico = carregar_historico()
    ordenado = sorted(historico, key=lambda x: x["score"], reverse=True)
    return ordenado[:top]

