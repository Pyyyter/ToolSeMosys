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

#region Manipulação de tabelas em memória

def substituir_primeira_coluna(tabela, vetor, starting_index=0):
	if len(tabela) == len(vetor):
		for i in range(len(tabela)):
			try:
				tabela[i+starting_index][0] = vetor[i]
			except:
				pass	
	else:
		print("O número de linhas na matriz não é igual ao número de elementos no vetor.")

def remover_primeira_coluna(tabela):
	return [linha[1:] for linha in tabela]

def remover_primeira_linha(tabela):
	return tabela[1:]

def reduzir_tabela_com_media(tabela_original, novo_tamanho, timeslices):
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


	for i in range(len(nova_tabela)):
		nova_tabela[i].insert(0,timeslices[i])

	nova_tabela.insert(0,tabela_original[0])

	return nova_tabela

def reduzir_tabela_com_soma(tabela_original, novo_tamanho, timeslices):
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

	for i in range(len(nova_tabela)):
		nova_tabela[i].insert(0,timeslices[i])

	nova_tabela.insert(0,tabela_original[0])

	return nova_tabela

def cortar_tabela(tabela, p, q):
	"""
	Função que literalmente corta uma tabela de tamamho MxN para PxQ, jogando fora as linhas e colunas excedentes.
	"""
	if p > len(tabela) or q > len(tabela[-1]):
		print("A nova tabela é maior que a tabela original.")
		return None

	nova_tabela = [linha[:q] for linha in tabela[:p]]
	return nova_tabela

#endregion

#region manipulação direta de I/O usando arquivos

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
				break  

		if indice_inicio and indice_fim :
			linhas_substituidas = linhas[:indice_inicio + 1]  # Mantém as linhas antes da tabela
			for linha in nova_tabela:
				linhas_substituidas.append(' '.join(map(str, linha)) + '\n') 
			linhas_substituidas.extend(linhas[indice_fim:]) # Mantém as linhas depois da tabela
			with open(caminho_arquivo, 'w') as arquivo:
				arquivo.writelines(linhas_substituidas)
		else:
			print("Não foi possível encontrar a tabela no arquivo.")
	except:
		print("Erro na função substituir tabela.")

def substituir_linha_em_arquivo(nome_arquivo, antiga_string, nova_string):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    for i, linha in enumerate(linhas):
        if antiga_string in linha:
            linhas[i] = nova_string + '\n'
            break

    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)

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

def atualizar_param(param, caminho_arquivo, timeslices, metodo):
	'''
	Atualiza o parâmetro especificado com o novo tamanho. Se o método for 0, a tabela é reduzida com soma. Se for 1, a tabela é reduzida com média.
	'''
	if metodo == 0:
		for tabela in lerParams(param, caminho_arquivo):
			substituir_tabela(caminho_arquivo, reduzir_tabela_com_soma(ler_tabela(caminho_arquivo, tabela), len(timeslices), timeslices), tabela)
	elif metodo == 1:
		for tabela in lerParams(param, caminho_arquivo):
			substituir_tabela(caminho_arquivo, reduzir_tabela_com_media(ler_tabela(caminho_arquivo, tabela), len(timeslices), timeslices), tabela)
#endregion

#region leitura de informações e criação de timeslices
def gerar_timeslices(seasons, daytypes, dailytimebrackets):
	"""
	Função que recebe o caminho do arquivo, o nome da tabela e o novo tamanho e retorna a tabela com o novo tamanho.
	"""
	timeslices = []
	for season in seasons:
		for daytype in daytypes:
			for dailytimebracket in dailytimebrackets:
				timeslices.append("S"+season+"D"+daytype+"T"+dailytimebracket)
	return timeslices

def ler_season(timeslice):
	'''
	Função que retorna a season de um timeslice
	'''
	return timeslice[1]	

def ler_daytype(timeslice):
	'''
	Função que retorna a daytype de um timeslice
	'''
	return timeslice[3]

def ler_dailytimebracket(timeslice):
	'''
	Função que retorna a dailytimebracket de um timeslice
	'''
	return timeslice[5]
#endregion

#region criação de tabelas de conversão

def gerar_linha_conversionld(timeslice, daytypes):
	linha = []
	for daytype in daytypes:
		if daytype == ler_daytype(timeslice):
			linha.append('1')
		else:
			linha.append('0')
	return linha

def gerar_linha_conversionls(timeslice, seasons):
	linha = []
	for season in seasons:
		if season == ler_season(timeslice):
			linha.append('1')
		else:
			linha.append('0')
	return linha

def gerar_linha_conversionlh(timeslice, dailytimebrackets):
	linha = []
	for dailytimebracket in dailytimebrackets:
		if dailytimebracket == ler_dailytimebracket(timeslice):
			linha.append('1')
		else:
			linha.append('0')
	return linha

def gerar_conversionls(timeslices, seasons):
	conversionls = []
	for timeslice in timeslices:
		conversionls.append(gerar_linha_conversionls(timeslice, seasons))

	for i in range(len(conversionls)):
		conversionls[i].insert(0,timeslices[i])

	conversionls.insert(0,seasons)

	return conversionls

def gerar_conversionlh(timeslices, dailytimebrackets):
	conversionlh = []
	for timeslice in timeslices:
		conversionlh.append(gerar_linha_conversionlh(timeslice, dailytimebrackets))

	for i in range(len(conversionlh)):
		conversionlh[i].insert(0,timeslices[i])

	conversionlh.insert(0,dailytimebrackets)

	return conversionlh

def gerar_conversionld(timeslices, daytypes):
	conversionld = []
	for timeslice in timeslices:
		conversionld.append(gerar_linha_conversionld(timeslice, daytypes)) 

	for i in range(len(conversionld)):
		conversionld[i].insert(0,timeslices[i])

	conversionld.insert(0,seasons)

	return conversionld

#endregion

#region manipulação de parâmetros

def atualizar_daytypes(daytypes, arquivo):
	substituir_linha_em_arquivo(arquivo, 'DAYTYPE', 'set DAYTYPE := ' + ' '.join(daytypes)+ ';')

def atualizar_seasons(seasons, arquivo):
	substituir_linha_em_arquivo(arquivo, 'SEASON', 'set SEASON := ' + ' '.join(seasons)+ ';')

def atualizar_dailytimebrackets(daylytimebrackets, arquivo):
	substituir_linha_em_arquivo(arquivo, 'DAILYTIMEBRACKET', 'set DAILYTIMEBRACKET := ' + ' '.join(daylytimebrackets)+ ';')

def atualizar_timeslices(timeslices, arquivo):
	substituir_linha_em_arquivo(arquivo, 'TIMESLICE', 'set TIMESLICE := ' + ' '.join(timeslices)+ ';')

#endregion

def atualizar_arquivo(arquivo, daytypes, seasons, dailytimebrackets):
	timeslices = gerar_timeslices(seasons, daytypes, dailytimebrackets)
	atualizar_daytypes(daytypes, arquivo)
	atualizar_seasons(seasons, arquivo)
	atualizar_dailytimebrackets(dailytimebrackets, arquivo)
	atualizar_timeslices(timeslices, arquivo)
	substituir_tabela(arquivo, gerar_conversionld(timeslices, daytypes), 'Conversionld')
	substituir_tabela(arquivo, gerar_conversionlh(timeslices, dailytimebrackets), 'Conversionlh')
	substituir_tabela(arquivo, gerar_conversionls(timeslices, seasons), 'Conversionls')
	substituir_tabela(arquivo, reduzir_tabela_com_soma(ler_tabela(arquivo, 'YearSplit'), len(timeslices), timeslices), 'YearSplit')
	atualizar_param('SpecifiedDemandProfile', arquivo, timeslices, 0)
	atualizar_param('CapacityFactor', arquivo, timeslices, 1)
#endregion

caminho_arquivo = 'sys_ex.txt'
nome_param = "CapacityFactor"

#daytypes = ['1','2']
#seasons = ['1','2']
#dailytimebrackets = ['1','2','3','4']
daytypes = ['1', '2']
seasons = ['1','2']
dailytimebrackets = ['1','2']
atualizar_arquivo(caminho_arquivo, daytypes, seasons, dailytimebrackets)