import random
from historico import salvar_analise

def processar_fechamento(pool, resultado, fechamento):
    linhas = []
    melhor = {"linha": None, "pontos": -1, "numeros": []}
    resultado_set = set(resultado)

    for i, indices in enumerate(fechamento, start=1):
        numeros = [pool[idx] for idx in indices if idx < len(pool)]
        pontos = len(resultado_set.intersection(numeros))

        info = {
            "linha": i,
            "numeros": numeros,
            "pontos": pontos
        }

        linhas.append(info)

        if pontos > melhor["pontos"]:
            melhor = info

    return linhas, melhor

def gerar_jogos(numeros, quantidade=6):
    base = list(set(numeros))
    if len(base) < 6:
        return []

    jogos = []
    for _ in range(quantidade):
        jogos.append(sorted(random.sample(base, 6)))
    return jogos

def score_nucleo21(media, frequencia):
    return round((media * frequencia) / 10, 2)

def analisar_e_salvar(pool, resultado, fechamento, fechamento_nome):
    linhas, melhor = processar_fechamento(pool, resultado, fechamento)
    jogos = gerar_jogos(melhor["numeros"])

    salvar_analise(
        resultado=resultado,
        fechamento=fechamento_nome,
        melhor_linha=melhor["linha"],
        pontos=melhor["pontos"],
        jogos=jogos
    )

    return linhas, melhor, jogos
