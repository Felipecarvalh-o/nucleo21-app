import json
import os
from datetime import datetime

ARQUIVO = "historico.json"

def carregar_historico():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_analise(resultado, fechamento, melhor_linha, pontos, jogos):
    historico = carregar_historico()

    registro = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "resultado": resultado,
        "fechamento": fechamento,
        "melhor_linha": melhor_linha,
        "pontos": pontos,
        "jogos": jogos
    }

    historico.append(registro)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def ranking_jogos():
    historico = carregar_historico()
    ranking = {}

    for reg in historico:
        resultado = set(reg["resultado"])
        for jogo in reg["jogos"]:
            chave = tuple(sorted(jogo))
            pontos = len(resultado.intersection(jogo))

            if chave not in ranking:
                ranking[chave] = {"total": 0, "vezes": 0}

            ranking[chave]["total"] += pontos
            ranking[chave]["vezes"] += 1

    ranking_final = []
    for jogo, dados in ranking.items():
        media = dados["total"] / dados["vezes"]
        ranking_final.append((list(jogo), media, dados["vezes"]))

    ranking_final.sort(key=lambda x: x[1], reverse=True)
    return ranking_final

def exportar_historico():
    historico = carregar_historico()
    linhas = ["data,fechamento,melhor_linha,pontos"]

    for h in historico:
        linhas.append(
            f"{h['data']},{h['fechamento']},{h['melhor_linha']},{h['pontos']}"
        )

    return "\n".join(linhas)
