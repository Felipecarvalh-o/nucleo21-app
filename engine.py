from itertools import combinations

# ======================================================
# UTILIDADES BÁSICAS
# ======================================================

def calcular_score(numeros, resultado):
    """
    Calcula quantos acertos um jogo teve em relação ao resultado.
    """
    return len(set(numeros) & set(resultado))


# ======================================================
# NÚCLEO INTELIGENTE (existente)
# ======================================================

def processar_fechamento(pool, resultado, fechamento):
    """
    Avalia todas as linhas de um fechamento e retorna:
    - todas as linhas avaliadas
    - a melhor linha (maior pontuação)
    """
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
    Gera jogos a partir de um núcleo base (usado no Núcleo Inteligente).
    Retorna até 6 jogos.
    """
    return [list(j) for j in combinations(sorted(numeros_base), 6)][:6]


# ======================================================
# 🟣 NÚCLEO EXPANDIDO 25™ (NOVO)
# ======================================================

def validar_dezenas_25(dezenas):
    """
    Valida se a entrada possui exatamente 25 dezenas válidas da Mega-Sena.
    """
    if not isinstance(dezenas, list):
        return False, "Entrada inválida."

    dezenas = sorted(set(dezenas))

    if len(dezenas) != 25:
        return False, "Você deve informar exatamente 25 dezenas."

    if any(n < 1 or n > 60 for n in dezenas):
        return False, "As dezenas devem estar entre 1 e 60."

    return True, dezenas


def gerar_jogos_nucleo25(dezenas_25, limite=190):
    """
    Estratégia 🟣 Núcleo Expandido 25™

    Conceito:
    - Usuário escolhe 25 dezenas
    - Geração estruturada de jogos de 6 dezenas
    - Volume controlado (190 jogos)
    - Estratégia educacional e estatística

    Retorno:
    - Lista com até 190 jogos
    """

    valido, resultado = validar_dezenas_25(dezenas_25)
    if not valido:
        raise ValueError(resultado)

    dezenas = resultado

    # Todas as combinações possíveis de 6 dezenas
    todas_combinacoes = combinations(dezenas, 6)

    jogos = []
    for jogo in todas_combinacoes:
        jogos.append(list(jogo))
        if len(jogos) >= limite:
            break

    return jogos
