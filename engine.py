from itertools import combinations
import random

def processar_fechamento(pool, resultado, indices_linhas):
    melhor = {"linha": 0, "pontos": -1, "numeros": []}
    linhas_processadas = []

    for i, indices in enumerate(indices_linhas):
        linha = [pool[idx] for idx in indices]
        acertos = set(linha).intersection(resultado)
        pontos = len(acertos)

        linhas_processadas.append({
            "linha": i + 1,
            "numeros": linha,
            "pontos": pontos,
            "acertos": acertos
        })

        if pontos > melhor["pontos"]:
            melhor = {
                "linha": i + 1,
                "pontos": pontos,
                "numeros": linha
            }

    return linhas_processadas, melhor


def gerar_jogos(melhor_linha, limite=6):
    jogos = []
    combinacoes = list(combinations(melhor_linha, 6))
    random.shuffle(combinacoes)

    for c in combinacoes[:limite]:
        jogos.append(sorted(c))

    return jogos
