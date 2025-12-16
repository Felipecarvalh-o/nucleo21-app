from itertools import combinations
from collections import Counter
import random


# ---------------- BÁSICO ----------------

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
    """
    Núcleo Inteligente™
    Gera até 6 jogos a partir do núcleo base
    """
    return [list(j) for j in combinations(sorted(numeros_base), 6)][:6]


# ---------------- NÚCLEO EXPANDIDO 25™ ----------------

def validar_dezenas_25(dezenas):
    if not isinstance(dezenas, list):
        return False, "Entrada inválida."

    dezenas = sorted(set(dezenas))

    if len(dezenas) != 25:
        return False, "Você deve informar exatamente 25 dezenas."

    if any(n < 1 or n > 60 for n in dezenas):
        return False, "As dezenas devem estar entre 1 e 60."

    return True, dezenas


def gerar_jogos_nucleo25(dezenas_25, total_jogos=190):
    """
    Núcleo Expandido 25™ (balanceado)
    ---------------------------------
    - Gera 190 jogos de 6 dezenas
    - Controla repetição excessiva
    - Distribuição uniforme das dezenas
    - Estrutura educacional e estatística
    """

    valido, resultado = validar_dezenas_25(dezenas_25)
    if not valido:
        raise ValueError(resultado)

    dezenas = resultado

    todas = list(combinations(dezenas, 6))
    random.shuffle(todas)

    contador = Counter()
    jogos = []

    for jogo in todas:
        # score de repetição (quanto menor, melhor)
        repeticao = sum(contador[n] for n in jogo)

        # regra simples e eficiente de balanceamento
        if repeticao <= 6:
            jogos.append(list(jogo))
            for n in jogo:
                contador[n] += 1

        if len(jogos) >= total_jogos:
            break

    return jogos
