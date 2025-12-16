from itertools import combinations
import random


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


def gerar_jogos(numeros_base, limite=6):
    """
    Núcleo Inteligente™
    """
    combs = list(combinations(sorted(numeros_base), 6))
    random.shuffle(combs)
    return [list(c) for c in combs[:limite]]


# ===================================================
# 🟣 NÚCLEO EXPANDIDO 25™ — FECHAMENTO REAL
# ===================================================

def validar_dezenas_25(dezenas):
    dezenas = sorted(set(dezenas))

    if len(dezenas) != 25:
        return False, "Informe exatamente 25 dezenas."

    if any(n < 1 or n > 60 for n in dezenas):
        return False, "As dezenas devem estar entre 1 e 60."

    return True, dezenas


def gerar_jogos_nucleo25(dezenas_25, total_jogos=190):
    """
    Núcleo Expandido 25™
    Estratégia com distribuição balanceada
    (não usa primeiras combinações)
    """

    valido, dezenas = validar_dezenas_25(dezenas_25)
    if not valido:
        raise ValueError(dezenas)

    todas = list(combinations(dezenas, 6))

    # 🔹 Embaralha para evitar jogos colados
    random.shuffle(todas)

    selecionados = []
    freq = {n: 0 for n in dezenas}

    for jogo in todas:
        # Evita sobrecarga de dezenas
        if all(freq[n] < (total_jogos * 6 / 25) + 2 for n in jogo):
            selecionados.append(list(jogo))
            for n in jogo:
                freq[n] += 1

        if len(selecionados) >= total_jogos:
            break

    return selecionados
