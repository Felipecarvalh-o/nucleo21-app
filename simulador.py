import random

def sortear():
    """Gera um sorteio aleatório com 6 dezenas"""
    return sorted(random.sample(range(1, 61), 6))


def pontuar(jogo, sorteio):
    """Conta quantos acertos"""
    return len(set(jogo) & set(sorteio))


def simular_cenario(jogos, simulacoes=500):
    """
    Simula vários sorteios aleatórios e avalia os jogos
    Retorna estatísticas educacionais
    """
    resultados = []

    for _ in range(simulacoes):
        sorteio = sortear()
        melhor_ponto = max(pontuar(jogo, sorteio) for jogo in jogos)
        resultados.append(melhor_ponto)

    return {
        "media": round(sum(resultados) / len(resultados), 2),
        "maximo": max(resultados),
        "zeros": resultados.count(0),
        "acima_4": len([r for r in resultados if r >= 4])
    }
