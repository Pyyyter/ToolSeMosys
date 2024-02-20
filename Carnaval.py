#region test
# import Lock
# lock = lock()
# def substituicaoAssincrona(nome_arquivo, nome_tabela, novo_tamanho, lock):
# 	if lock.locked():
# 		substituicaoAssincrona(nome_arquivo, nome_tabela, novo_tamanho, lock)
# 		return
# 	lock.acquire()
# 	tabela = ler_tabela(nome_arquivo, nome_tabela)
# 	nova_tabela = reduzir_tabela(tabela, novo_tamanho)
# 	substituir_tabela(nome_arquivo, nova_tabela, nome_tabela)
# 	lock.release()
#endregion

#region functions
def delimita_inicio_da_tabela(linha, nome_da_tabela):
	if nome_da_tabela.strip() in linha.strip():
		return True
	
def delimita_fim_da_tabela(linha):
	if ('[' in linha.strip() or ';' in linha.strip()) or not linha.strip():
		return True

def ler_tabela(nome_arquivo, nome_tabela):
	tabela = []
	encontrou_tabela = False
	try:
			with open(nome_arquivo, 'r') as arquivo:
					for linha in arquivo:
							if delimita_inicio_da_tabela(linha, nome_tabela):
								encontrou_tabela = True
								continue
							if encontrou_tabela and delimita_fim_da_tabela(linha):
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

	# Povoamento da matriz nova
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
	try:
		with open(caminho_arquivo, 'r') as arquivo:
			linhas = arquivo.readlines()

		indice_inicio = None
		indice_fim = None
		encontrou_tabela = False
		for i, linha in enumerate(linhas):
			if delimita_inicio_da_tabela(linha, nome_tabela): # critério de início
				encontrou_tabela = True
				indice_inicio = i  
			elif encontrou_tabela and delimita_fim_da_tabela(linha): # critério de parada
				indice_fim = i
				break  # Parar de procurar

		# Substituir a tabela no arquivo pelo conteúdo da nova matriz
		if indice_inicio and indice_fim :
			linhas_substituidas = linhas[:indice_inicio + 1]  # Mantém as linhas antes da tabela
			for linha in nova_matriz:
				linhas_substituidas.append(' '.join(map(str, linha)) + '\n') 
			linhas_substituidas.extend(linhas[indice_fim:])  

			# Escrever o conteúdo de volta no arquivo
			with open(caminho_arquivo, 'w') as arquivo:
				arquivo.writelines(linhas_substituidas)
		else:
			print("Não foi possível encontrar a tabela no arquivo.")
	except:
		print("Erro na função substituir tabela.")

def lerParams(param, caminho_arquivo):
	nome_das_tabelas = []
	
	encontrou_tabela = False
	with open(caminho_arquivo, 'r') as arquivo:
					for linha in arquivo:
							if param.strip() in linha.strip():
									encontrou_tabela = True
									continue  
							if encontrou_tabela and ';' in linha:
								break
							if encontrou_tabela and '[' in linha and linha.strip():
									linha = linha.strip()
									nome_das_tabelas.append(linha)
	return nome_das_tabelas

def reduzir_matriz(matriz, p, q):
	if p > len(matriz) or q > len(matriz[-1]):
		print("A nova matriz é maior que a matriz original.")
		return None

	nova_matriz = [linha[:q] for linha in matriz[:p]]
	return nova_matriz
#endregion

caminho_arquivo = 'Atlantis_base/atlantis_v2copy.txt'
nome_param = "EmissionActivityRatio"
novo_tamanho = 1
nome_das_tabelas = lerParams(nome_param, caminho_arquivo)
tabelas_diferentes = ['Conversionld', 'Conversionls', 'Conversionlh']

try :
	for nome_da_tabela in nome_das_tabelas:
		substituir_tabela(caminho_arquivo, reduzir_tabela(ler_tabela(caminho_arquivo, nome_da_tabela), novo_tamanho), nome_da_tabela)
except:
	pass

for tabelas_diferente in tabelas_diferentes:
	if tabelas_diferente == 'Conversionld':
		substituir_tabela(caminho_arquivo, reduzir_matriz(ler_tabela(caminho_arquivo,tabelas_diferente),2,2), tabelas_diferente)
	if tabelas_diferente == 'Conversionls':
		substituir_tabela(caminho_arquivo, reduzir_matriz(ler_tabela(caminho_arquivo, tabelas_diferente), 2, 2), tabelas_diferente)
	if tabelas_diferente == 'Conversionlh':
		substituir_tabela(caminho_arquivo, reduzir_matriz(ler_tabela(caminho_arquivo, tabelas_diferente), 2, 2), tabelas_diferente)
