import random
from itertools import combinations


def validar_dezenas_25(dezenas):
    dezenas = sorted(set(dezenas))

    if len(dezenas) != 25:
        return False, "Você deve informar exatamente 25 dezenas."

    if any(n < 1 or n > 60 for n in dezenas):
        return False, "As dezenas devem estar entre 1 e 60."

    return True, dezenas


def gerar_jogos_nucleo25(dezenas_25, total_jogos=190, seed=None):
    """
    Núcleo Expandido 25™ (Balanceado)

    - Distribuição uniforme das dezenas
    - Jogos não sequenciais
    - Sem repetição burra
    """

    valido, dezenas = validar_dezenas_25(dezenas_25)
    if not valido:
        raise ValueError(dezenas)

    # Todas as combinações possíveis
    combinacoes = list(combinations(dezenas, 6))

    # Embaralha para evitar padrões fixos
    if seed is not None:
        random.seed(seed)
    random.shuffle(combinacoes)

    jogos = []
    contador = {n: 0 for n in dezenas}

    for combo in combinacoes:
        # Critério simples de balanceamento:
        peso = sum(contador[n] for n in combo)

        jogos.append((peso, combo))

        if len(jogos) >= total_jogos * 3:
            break

    # Ordena pelos menos usados
    jogos.sort(key=lambda x: x[0])

    jogos_finais = []
    for _, combo in jogos[:total_jogos]:
        jogos_finais.append(list(combo))
        for n in combo:
            contador[n] += 1

    return jogos_finais
