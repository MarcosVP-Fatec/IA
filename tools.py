def maxWidth(lista):
    """
    Verifica a maior largura dos itens caracteres da lista.
    """
    n_max = 0
    for item in lista:
        if len(item) > n_max:
            n_max = len(item)
    return n_max
