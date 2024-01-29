#Exercicio 1.1
def comprimento(lista):
	if lista == []:
		return 0
	return 1 + comprimento(lista[1:])
	pass

#Exercicio 1.2
def soma(lista):
	if lista == []:
		return 0
	return lista[0] + soma(lista[1:]) 
	pass

#Exercicio 1.3
def existe(lista, elem):
	if lista == []:
		return False
	if lista[0] == elem:
		return True
	return existe(lista[1:],elem)
	pass

#Exercicio 1.4
def concat(l1, l2):
	if l2 == []:
		return l1
	l1.append(l2[0])
	return concat(l1,l2[1:])
	pass

#Exercicio 1.5
def inverte(lista):
	if lista == []:
		return []
	return concat([lista[-1]], inverte(lista[:-1])) # tamos a usar o concat aqui em vez do +, só porque não convém usar a concatenação
	pass

#Exercicio 1.6
def capicua(lista):
	# return lista == inverte(lista): isto está bem, mas não tá recursivamente como os testes querem
	if comprimento(lista) <= 1: # tamos a usar a outra função também
		return True
	return lista[0] == lista[-1] and capicua(lista[1:-1])
	pass

#Exercicio 1.7
def concat_listas(lista):
	if(lista) == []:
		return []
	#return lista[0] + concat_listas(lista[1:]) esta era uma maneira
	return concat( lista[0],concat_listas(lista[1:]))
	pass

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []
	value = lista[0]
	if lista[0] == original:
		value = novo	
	return concat([value], substitui(lista[1:], original, novo))
	pass

#Exercicio 1.9
def fusao_ordenada(lista1, lista2):
	if lista2 == []:
		return lista1
	if lista1 == []:
		return lista2
	if lista1[0] < lista2[0]:
		return concat([lista1[0]], fusao_ordenada(lista1[1:], lista2 ))

	return concat([lista2[0]], fusao_ordenada(lista1, lista2[1:]))
	pass

#Exercicio 1.10
def lista_subconjuntos(lista):
	if lista == []:
		return [[]]
	subconj = lista_subconjuntos(lista[1:])
	return subconj + [[lista[0]] + subset for subset in subconj]
pass


#Exercicio 2.1
def separar(lista):
	if lista == []:
		return [], []
	a1,b1 = lista[0]
	lista_a1, lista_b1 = separar(lista[1:])
	return [a1]+ lista_a1, [b1] + lista_b1
	pass

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if lista == []:
		return ([],0)
	
	NewList, count = remove_e_conta(lista[1:], elem)
	if lista[0] == elem:
		return (NewList ,count+1)
	else:
		NewList = [lista[0]] + NewList# não se podia pôr NewList += [lista[0]] porque senão a lista não vinha na ordem certa
		return (NewList ,count)
	pass

#Exercicio 2.3
def N_ocorrencias(lista):
	pass

#Exercicio 3.1
def cabeca(lista):
	if lista == []:
		return None
	else:
		return lista[0]
	pass

#Exercicio 3.2
def cauda(lista):
	if lista == []:
		return None
	else:
		return lista[1:]
	pass

#Exercicio 3.3
def juntar(l1, l2):
	if len(l1) != len(l2):
		return None
	if l1 == []:
		return []
	a1 = l1[0]
	b1 = l2[0]
    
	return [(a1,b1)] + juntar(l1[1:], l2[1:])
	pass

#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None
	
	Nmenor = menor(lista[1:])
	if Nmenor == None: # foi preciso meter aqui o NoneType, porque senão dava erro. A razão é porque na linha anterior percorremos a lista até estar vazia, logo retorna None como dizemos no If
		return lista[0]
	elif Nmenor < lista[0]:
		return Nmenor
	else:
		return lista[0]
	pass

#Exercício 3.5
def menor_e_lista(lista):
	if lista == []:
		return None,[]
	if len(lista) == 1:
		return lista[0], []
	
	Nmenor, Lrestante = menor_e_lista(lista[1:])
	if Nmenor == None: 
		return lista[0]
	elif Nmenor < lista[0]:
		return Nmenor, [lista[0]] + Lrestante
	else:
		return lista[0], [Nmenor] + Lrestante
	pass

#Exercicio 3.6
def max_min(lista):
    if lista == []:
        return None

    a1 = lista[0]
    b1 = lista[0]

    tail = max_min(lista[1:])

    if tail == None:
        return (a1, b1)

    max = tail[0]
    min = tail[1]

    if max > a1:
        if min < b1:
            return (max, min)
        else:
            return (max, b1)
    else:
        if min < b1:
            return (a1, min)
        else:
            return (a1, b1)