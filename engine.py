from itertools import combinations

def processar_fechamento(pool, resultado, fechamento):
    """
    Processa as linhas do fechamento e calcula pontos
    """
    linhas = []

    for i, linha in enumerate(fechamento, start=1):
        numeros = [pool[n - 1] for n in linha]
        pontos = len(set(numeros) & set(resultado))

        linhas.append({
            "linha": i,
            "numeros": numeros,
            "pontos": pontos
        })

    melhor = max(linhas, key=lambda x: x["pontos"])
    return linhas, melhor


def gerar_jogos(numeros_base, limite=6):
    """
    Gera jogos de 6 dezenas a partir da melhor linha
    """
    combinacoes = list(combinations(sorted(numeros_base), 6))
    jogos = []

    for combo in combinacoes[:limite]:
        jogos.append(" ".join(f"{n:02d}" for n in combo))

    return jogos


def calcular_score(linhas):
    """
    Calcula um score geral (0 a 10) baseado na performance
    """
    pesos = {
        6: 10,
        5: 7,
        4: 4,
        3: 2
    }

    total = 0
    maximo = len(linhas) * 10

    for linha in linhas:
        total += pesos.get(linha["pontos"], 0)

    if maximo == 0:
        return 0

    score = (total / maximo) * 10
    return round(score, 1)
