from itertools import combinations


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


def gerar_jogos_nucleo25(dezenas_25):
    """
    Estratégia Núcleo 25™
    --------------------
    Recebe 25 dezenas escolhidas pelo usuário e gera 190 jogos de 6 dezenas.

    Conceito:
    - Cobertura matemática estruturada
    - Foco em consistência e organização
    - Estratégia educacional (não garante prêmios)

    Retorno:
    - Lista com 190 jogos (cada jogo = lista de 6 dezenas)
    """

    valido, resultado = validar_dezenas_25(dezenas_25)
    if not valido:
        raise ValueError(resultado)

    dezenas = resultado

    # Gera todas as combinações possíveis de 6 dezenas
    todas_combinacoes = list(combinations(dezenas, 6))

    # Seleciona 190 jogos (padrão comercial do Núcleo 25™)
    jogos = todas_combinacoes[:190]

    # Converte para listas
    jogos = [list(jogo) for jogo in jogos]

    return jogos

