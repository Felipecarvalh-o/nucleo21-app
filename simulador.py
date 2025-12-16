import random


def simular_cenario(jogos, total_sorteios=500):
    """
    🧪 Simulação Estatística de Cenários

    Executa sorteios aleatórios independentes e avalia,
    em cada cenário, o melhor desempenho observado entre os jogos.

    Importante:
    - Uso estatístico e educacional
    - Não representa previsão
    - Não indica garantia de resultado futuro
    """

    desempenhos_observados = []
    cenarios_sem_pontuacao = 0
    melhor_desempenho_observado = 0

    for _ in range(total_sorteios):
        sorteio = set(random.sample(range(1, 61), 6))
        melhor_no_cenario = 0

        for jogo in jogos:
            pontos = len(sorteio & set(jogo))
            melhor_no_cenario = max(melhor_no_cenario, pontos)

        desempenhos_observados.append(melhor_no_cenario)

        if melhor_no_cenario == 0:
            cenarios_sem_pontuacao += 1

        melhor_desempenho_observado = max(
            melhor_desempenho_observado, melhor_no_cenario
        )

    media_desempenho = round(
        sum(desempenhos_observados) / len(desempenhos_observados), 2
    )

    return {
        "media": media_desempenho,          # média de desempenho observado
        "maximo": melhor_desempenho_observado,  # melhor cenário observado
        "zeros": cenarios_sem_pontuacao,    # cenários sem pontuação
        "total": total_sorteios
    }
