import json
from datetime import datetime
from itertools import combinations

HISTORY_FILE = "history.json"


def calcular_score(numeros, resultado):
    return len(set(numeros) & set(resultado))


def processar_fechamento(pool, resultado, fechamento):
    linhas = []
    melhor = None

    for i, linha in enumerate(fechamento, 1):
        numeros = [pool[n - 1] for n in linha]
        pontos = calcular_score(numeros, resultado)

        data = {
            "linha": i,
            "numeros": numeros,
            "pontos": pontos
        }

        linhas.append(data)

        if not melhor or pontos > melhor["pontos"]:
            melhor = data

    salvar_historico(resultado, melhor)
    return linhas, melhor


def gerar_jogos(numeros_base):
    return [list(j) for j in combinations(sorted(numeros_base), 6)][:6]


def salvar_historico(resultado, melhor):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except:
        dados = {"analises": []}

    dados["analises"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "resultado": resultado,
        "melhor_linha": melhor["numeros"],
        "pontos": melhor["pontos"]
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def carregar_historico():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)["analises"]
    except:
        return []
