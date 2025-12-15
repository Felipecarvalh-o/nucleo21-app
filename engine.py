import random
import statistics

def processar_fechamento(pool, resultado, indices_linhas):
    """
    Processa as linhas do fechamento e calcula pontos
    """
    linhas = []
    melhor = {"linha": 0, "pontos": -1, "numeros": []}

    for i, indices in enumerate(indices_linhas, start=1):
        numeros = [pool[idx] for idx in indices if idx < len(pool)]
        acertos = set(numeros).intersection(resultado)
        pontos = len(acertos)

        linha_info = {
            "linha": i,
            "numeros": numeros,
            "pontos": pontos
        }
        linhas.append(linha_info)

        if pontos > melhor["pontos"]:
            melhor = linha_info

    return linhas, melhor


def gerar_jogos(numeros_base, qtd_jogos=6):
    """
    Gera jogos de 6 dezenas a partir da melhor linha
    """
    jogos = []

    if len(numeros_base) < 6:
        return jogos

    for _ in range(qtd_jogos):
        jogo = sorted(random.sample(numeros_base, 6))
        jogos.append(jogo)

    return jogos


def calcular_score(linhas):
    """
    Score Núcleo 21 (0 a 10)
    Baseado na média de pontos e consistência
    """
    pontos = [l["pontos"] for l in linhas]

    if not pontos:
        return 0

    media = statistics.mean(pontos)
    desvio = statistics.pstdev(pontos) if len(pontos) > 1 else 0

    # Fórmula simples, estável e explicável
    score = (media / 6) * 10

    # Penaliza volatilidade
    score -= desvio

    return max(0, min(score, 10))
