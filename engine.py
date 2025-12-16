from itertools import combinations
import random


def calcular_score(numeros, resultado):
    """
    Calcula a quantidade de dezenas coincidentes
    entre um conjunto analisado e um resultado passado.
    Uso estatístico / histórico.
    """
    return len(set(numeros) & set(resultado))


def processar_fechamento(pool, resultado, fechamento):
    """
    Avalia todas as linhas de um fechamento com base
    em um resultado histórico informado.

    Retorna:
    - lista completa de linhas avaliadas
    - linha com maior pontuação observada
    """

    linhas = []
    linha_destaque = None

    for i, linha in enumerate(fechamento, 1):
        numeros = [pool[n - 1] for n in linha if n > 0]
        pontos = calcular_score(numeros, resultado)

        data = {
            "linha": i,
            "numeros": numeros,
            "pontos": pontos  # pontuação observada (histórica)
        }

        linhas.append(data)

        if not linha_destaque or pontos > linha_destaque["pontos"]:
            linha_destaque = data

    return linhas, linha_destaque


def gerar_jogos(numeros_base, limite=6):
    """
    🍀 Núcleo Inteligente™

    Gera combinações a partir de um núcleo reduzido,
    utilizando critério de organização e amostragem.
    Não representa previsão ou garantia de resultado.
    """
    combs = list(combinations(sorted(numeros_base), 6))
    random.shuffle(combs)
    return [list(c) for c in combs[:limite]]


# ===================================================
# 🟣 NÚCLEO EXPANDIDO 25™ — DISTRIBUIÇÃO BALANCEADA
# ===================================================

def validar_dezenas_25(dezenas):
    dezenas = sorted(set(dezenas))

    if len(dezenas) != 25:
        return False, "Informe exatamente 25 dezenas distintas."

    if any(n < 1 or n > 60 for n in dezenas):
        return False, "As dezenas devem estar entre 1 e 60."

    return True, dezenas


def gerar_jogos_nucleo25(dezenas_25, total_jogos=190):
    """
    🍀 Núcleo Expandido 25™

    Estratégia de organização combinatória com
    controle de frequência das dezenas.
    Utiliza critérios estatísticos e não preditivos.
    """

    valido, dezenas = validar_dezenas_25(dezenas_25)
    if not valido:
        raise ValueError(dezenas)

    todas = list(combinations(dezenas, 6))
    random.shuffle(todas)

    selecionados = []
    freq = {n: 0 for n in dezenas}

    limite_freq = (total_jogos * 6 / 25) + 2

    for jogo in todas:
        if all(freq[n] < limite_freq for n in jogo):
            selecionados.append(list(jogo))
            for n in jogo:
                freq[n] += 1

        if len(selecionados) >= total_jogos:
            break

    return selecionados
