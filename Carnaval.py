def ler_tabela(nome_arquivo, nome_tabela):
	tabela = []
	encontrou_tabela = False
	try:
			with open(nome_arquivo, 'r') as arquivo:
					for linha in arquivo:
							if nome_tabela.strip() in linha.strip():
									encontrou_tabela = True
									continue  
							if encontrou_tabela and ('[' in linha or ';' in linha):
								break
							if encontrou_tabela and linha.strip():
									linha = linha.strip().split()
									tabela.append(linha)
							
			if not encontrou_tabela:
					print("Tabela não encontrada no arquivo.")
					return None
			return tabela

	except FileNotFoundError:
			print("O arquivo especificado não foi encontrado.")
			return None

def remover_primeira_coluna(matriz):
	return [linha[1:] for linha in matriz]
def remover_primeira_linha(matriz):
	return matriz[1:]

def reduzir_tabela(matriz_original, novo_tamanho):

	if (len(matriz_original)-1) % novo_tamanho != 0:
		return print("A matriz não é redutível para esse número de linhas")
	
	matriz_filtrada = remover_primeira_linha(remover_primeira_coluna(matriz_original))
	nova_matriz = []

	# Fator é a quantidade de linhas antigas serão combinadas para que uma nova seja criada
	fator = int(len(matriz_filtrada)/novo_tamanho)

	#povoamento da matriz nova
	for i in range(novo_tamanho):
		nova_matriz.append([])
		for j in range(len(matriz_original[1])-1):
			nova_matriz[i].append(1)

	for i in range(novo_tamanho):
		for j in range(len(matriz_filtrada[1])):
			soma = 0
			for k in range(fator):
				soma += float(matriz_filtrada[i*fator-k][j])
			nova_matriz[i][j] = soma/fator 
	nova_matriz.insert(0,matriz_original[0])
	for i in range(len(nova_matriz)):
		nova_matriz[i].insert(0,matriz_original[i][0])
	return nova_matriz

def substituir_tabela(caminho_arquivo, nova_matriz, nome_tabela):
    # Ler o conteúdo do arquivo
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Procurar a tabela dentro do conteúdo do arquivo
    indice_inicio = None
    indice_fim = None
    encontrou_tabela = False
    for i, linha in enumerate(linhas):
        if nome_tabela.strip() in linha.strip(): # critério de início
            encontrou_tabela = True
            indice_inicio = i  
        if encontrou_tabela and not linha.strip(): # critério de parada
            indice_fim = i
            break  # Parar de procurar

    # Substituir a tabela no arquivo pelo conteúdo da nova matriz
    if indice_inicio is not None and indice_fim is not None:
        linhas_substituidas = linhas[:indice_inicio + 1]  # Mantém as linhas antes da tabela
        for linha in nova_matriz:
            linhas_substituidas.append(' '.join(map(str, linha)) + '\n') 
        linhas_substituidas.extend(linhas[indice_fim:])  

        # Escrever o conteúdo de volta no arquivo
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.writelines(linhas_substituidas)
    else:
        print("Não foi possível encontrar a tabela no arquivo.")





nome_arquivo = 'Atlantis_base/atlantis_v2copy.txt'
nome_tabela = '[Atlantis_00A,EL_Services,*,*]'
novo_tamanho = 1


tabela = ler_tabela(nome_arquivo, nome_tabela)
nova_tabela = reduzir_tabela(tabela, novo_tamanho)
for linha in nova_tabela:
	print(linha)
substituir_tabela(nome_arquivo, nova_tabela, nome_tabela)
