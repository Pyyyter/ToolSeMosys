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
	"""
	Função que recebe o nome de um arquivo usando o nome de uma tabela e retorna a mesma em forma de lista de listas ( matriz ).
	"""
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

def remover_primeira_coluna(tabela):
	return [linha[1:] for linha in tabela]

def remover_primeira_linha(tabela):
	return tabela[1:]

def reduzir_tabela_com_media(tabela_original, novo_tamanho):
	"""
	Função que recebe uma tabela e um novo tamanho e retorna uma nova tabela com o tamanho especificado, fazendo a soma das linhas que foram agrupadas para a redução ocorrer.
	"""
	if (len(tabela_original)-1) % novo_tamanho != 0:
		return print("A tabela não é redutível para esse número de linhas")
	
	tabela_filtrada = remover_primeira_linha(remover_primeira_coluna(tabela_original))
	nova_tabela = []

	# Fator é a quantidade de linhas antigas serão combinadas para que uma nova seja criada
	fator = int(len(tabela_filtrada)/novo_tamanho)

	# Povoamento da tabela nova
	for i in range(novo_tamanho):
		nova_tabela.append([])
		for j in range(len(tabela_original[1])-1):
			nova_tabela[i].append(1)

	for i in range(novo_tamanho):
		for j in range(len(tabela_filtrada[1])):
			soma = 0
			for k in range(fator):
				soma += float(tabela_filtrada[i*fator-k][j])
			nova_tabela[i][j] = soma/fator

	nova_tabela.insert(0,tabela_original[0])

	for i in range(len(nova_tabela)):
		nova_tabela[i].insert(0,tabela_original[i][0])
	return nova_tabela

def reduzir_tabela_com_soma(tabela_original, novo_tamanho):
	"""
	Função que recebe uma tabela e um novo tamanho e retorna uma nova tabela com o tamanho especificado, fazendo a soma das linhas que foram agrupadas para a redução ocorrer.
	"""
	if (len(tabela_original)-1) % novo_tamanho != 0:
		return print("A tabela não é redutível para esse número de linhas")
	
	tabela_filtrada = remover_primeira_linha(remover_primeira_coluna(tabela_original))
	nova_tabela = []

	# Fator é a quantidade de linhas antigas serão combinadas para que uma nova seja criada
	fator = int(len(tabela_filtrada)/novo_tamanho)

	# Povoamento da tabela nova
	for i in range(novo_tamanho):
		nova_tabela.append([])
		for j in range(len(tabela_original[1])-1):
			nova_tabela[i].append(1)

	for i in range(novo_tamanho):
		for j in range(len(tabela_filtrada[1])):
			soma = 0
			for k in range(fator):
				soma += float(tabela_filtrada[i*fator-k][j])
			nova_tabela[i][j] = soma

	nova_tabela.insert(0,tabela_original[0])

	for i in range(len(nova_tabela)):
		nova_tabela[i].insert(0,tabela_original[i][0])
	return nova_tabela

def substituir_tabela(caminho_arquivo, nova_tabela, nome_tabela):
	"""
	Função que recebe a tabela nova, o nome da tabela e o caminho do arquivo e substitui a tabela no arquivo pela tabela passada por parâmetro.
	"""
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

		# Substituir a tabela no arquivo pelo conteúdo da nova tabela
		if indice_inicio and indice_fim :
			linhas_substituidas = linhas[:indice_inicio + 1]  # Mantém as linhas antes da tabela
			for linha in nova_tabela:
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
	'''
	Retorna uma lista de strings com o nome das tabelas que estão contidas no parâmetro especificado.
	'''
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

def cortar_tabela(tabela, p, q):
	"""
	Função que literalmente corta uma tabela de tamamho MxN para PxQ, jogando fora as linhas e colunas excedentes.
	"""
	if p > len(tabela) or q > len(tabela[-1]):
		print("A nova tabela é maior que a tabela original.")
		return None

	nova_tabela = [linha[:q] for linha in tabela[:p]]
	return nova_tabela

def gerar_timeslices(seasons, daytypes, dailytimebrackets):
	"""
	Função que recebe o caminho do arquivo, o nome da tabela e o novo tamanho e retorna a tabela com o novo tamanho.
	"""
	timeslices = []
	for season in seasons:
		for daytype in daytypes:
			for dailytimebracket in dailytimebrackets:
				timeslices.append("S"+str(season)+"D"+str(daytype)+"T"+str(dailytimebracket))
	return timeslices
#endregion

caminho_arquivo = 'Atlantis_base/atlantis_v2copy.txt'
nome_param = "CapacityFactor"
novo_tamanho = 1
nome_das_tabelas = lerParams(nome_param, caminho_arquivo)
tabelas_diferentes = ['Conversionld', 'Conversionls', 'Conversionlh']

# try :
# 	for nome_da_tabela in nome_das_tabelas:
# 		substituir_tabela(caminho_arquivo, reduzir_tabela_com_soma(ler_tabela(caminho_arquivo, nome_da_tabela), novo_tamanho), nome_da_tabela)
# except:
# 	pass
timeslices = gerar_timeslices([1,2,3,4], [1,2], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
print(timeslices)

# for tabelas_diferente in tabelas_diferentes:
# 	if tabelas_diferente == 'Conversionld':
# 		substituir_tabela(caminho_arquivo, reduzir_tabela(ler_tabela(caminho_arquivo,tabelas_diferente),2,2), tabelas_diferente)
# 	if tabelas_diferente == 'Conversionls':
# 		substituir_tabela(caminho_arquivo, reduzir_tabela(ler_tabela(caminho_arquivo, tabelas_diferente), 2, 2), tabelas_diferente)
# 	if tabelas_diferente == 'Conversionlh':
# 		substituir_tabela(caminho_arquivo, reduzir_tabela(ler_tabela(caminho_arquivo, tabelas_diferente), 2, 2), tabelas_diferente)
