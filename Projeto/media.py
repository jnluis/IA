def calcular_medias(nome_do_arquivo):
    # Abrir o arquivo para leitura
    with open(nome_do_arquivo, 'r') as arquivo:
        # Ler todas as linhas do arquivo
        linhas = arquivo.readlines()

    # Inicializar uma lista para armazenar as somas e as contagens
    somas = []
    contagens = []

    for linha in linhas:
        # Dividir a linha em colunas (assumindo que são separadas por espaços)
        colunas = linha.split()

        # Certificar-se de que a lista de somas tem o mesmo tamanho que o número de colunas
        while len(somas) < len(colunas):
            somas.append(0)
            contagens.append(0)

        # Adicionar os valores de cada coluna à soma correspondente
        for i, valor in enumerate(colunas):
            try:
                somas[i] += float(valor)
                contagens[i] += 1
            except ValueError:
                # Ignorar valores que não são números
                pass

    # Calcular a média para cada coluna
    medias = [soma / count if count != 0 else 0 for soma, count in zip(somas, contagens)]

    return medias

# Exemplo de uso
nome_do_arquivo = "score.txt"
medias = calcular_medias(nome_do_arquivo)
print("Médias por coluna:", medias)
