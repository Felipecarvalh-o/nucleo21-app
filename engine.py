from historico import salvar_analise

def processar_fechamento(pool, resultado, fechamento):
    linhas = []
    melhor = {
        "linha": None,
        "pontos": -1,
        "numeros": []
    }

    resultado_set = set(resultado)

    for i, indices in enumerate(fechamento, start=1):
        numeros_linha = [pool[idx] for idx in indices if idx < len(pool)]
        pontos = len(resultado_set.intersection(numeros_linha))

        linha_info = {
            "linha": i,
            "numeros": numeros_linha,
            "pontos": pontos
        }

        linhas.append(linha_info)

        if pontos > melhor["pontos"]:
            melhor = linha_info

    return linhas, melhor


def gerar_jogos(numeros_linha, quantidade=6):
    import random

    jogos = []
    base = list(set(numeros_linha))

    if len(base) < 6:
        return jogos

    for _ in range(quantidade):
        jogo = sorted(random.sample(base, 6))
        jogos.append(jogo)

    return jogos


def analisar_e_salvar(pool, resultado, fechamento, fechamento_nome):
    """
    Função central que:
    - processa o fechamento
    - gera jogos
    - salva no histórico
    """

    linhas, melhor = processar_fechamento(pool, resultado, fechamento)
    jogos = gerar_jogos(melhor["numeros"])

    salvar_analise(
        resultado=resultado,
        fechamento=fechamento_nome,
        melhor_linha=melhor["linha"],
        pontos=melhor["pontos"],
        jogos=jogos
    )

    return linhas, melhor, jogos
