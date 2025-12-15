def converter_lista(texto):
    try:
        return [int(n) for n in texto.replace(',', ' ').split()]
    except:
        return []

def validar_pool(pool):
    if len(pool) != 60:
        return False, "O pool deve conter exatamente 60 dezenas."
    if len(set(pool)) != 60:
        return False, "Existem dezenas repetidas."
    if min(pool) < 1 or max(pool) > 60:
        return False, "As dezenas devem estar entre 1 e 60."
    return True, ""
