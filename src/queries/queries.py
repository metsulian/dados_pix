# Selecionar as Regioes Unicas -> array -> adicionar "TODAS" a primeira entrada desse array
# Selecionar os valores unicos de AnoMes e ordenar em ordem crescente
# Filtrar dados da regiao selecionada


def get_regioes(engine):
    query = """
        SELECT DISTINCT "Regiao"
        FROM "DadosAPI"
    """

