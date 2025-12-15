from itertools import combinations


def calcular_score(numeros, resultado):
    return len(set(numeros) & set(resultado))


def processar_fechamento(pool, resultado, fechamento):
    linhas = []
    melhor = None

    for i, linha in enumerate(fechamento, 1):
        numeros = [pool[n - 1] for n in linha if n > 0]
        pontos = calcular_score(numeros, resultado)

        data = {
            "linha": i,
            "numeros": numeros,
            "pontos": pontos
        }

        linhas.append(data)

        if not melhor or pontos > melhor["pontos"]:
            melhor = data

    return linhas, melhor


def gerar_jogos(numeros_base):
    return [list(j) for j in combinations(sorted(numeros_base), 6)][:6]
