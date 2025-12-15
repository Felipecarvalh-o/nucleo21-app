def converter_lista(texto):
    """
    Converte uma string com números separados por espaço, vírgula ou traço
    em uma lista de inteiros únicos e ordenados.
    """
    if not texto:
        return []

    separadores = [",", ";", "-", "\n"]
    for sep in separadores:
        texto = texto.replace(sep, " ")

    try:
        numeros = list(set(int(n) for n in texto.split() if n.strip()))
        numeros.sort()
        return numeros
    except ValueError:
        return []


def validar_pool(pool):
    """
    Valida a base de dezenas (pool).
    """
    if not pool:
        return False, "A base de dezenas está vazia."

    if any(n < 1 or n > 60 for n in pool):
        return False, "Todas as dezenas devem estar entre 1 e 60."

    if len(pool) < 6:
        return False, "A base deve conter pelo menos 6 dezenas."

    if len(pool) > 60:
        return False, "A base não pode ter mais de 60 dezenas."

    if len(pool) != len(set(pool)):
        return False, "Existem dezenas repetidas na base."

    return True, None
