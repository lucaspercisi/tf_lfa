#retorna true se o parametro ja foi adicionado no afnd
def addedChar_afnd(char):

    for state in range(0,len(afnd)):
        if afnd[state][2] == char:
            return True
    return False


#busca a posição do parametro dentro do afnd
def bucaPosChar_afnd(char):

    for state in range(0,len(afnd)):
        if afnd[state][2] == char:
            if afnd[state][0][0]:
                return state
    return -1


#adiciona os tokens do arquivo em uma lista
tokens = []
f = open('tokens_GRs.txt','r')
for line in f:
    tokens.append(line)
f.close()

#remove os '\n' dos tokens
for i, token in enumerate(tokens):
    pos = token.find('\n')
    if pos > -1:
        token = token[:pos]
    tokens[i] = token
print ('TOKENS: ',tokens)


#carrega o afnd
afnd = []
state = 0
for token in range(0, len(tokens)):
    for char in range(0, len(tokens[token])):
        
        if char == 0: #ESTADO INICIAL TOKEN
            
            if not addedChar_afnd(tokens[token][char]):#NÃO FOI ADICIONADO

                afnd.append([(True,state),[state+1],tokens[token][char]])
                state = state + 1

            else:#JÁ FOI ADICIONADO
                
                pos = bucaPosChar_afnd(tokens[token][char]) #ENCONTRA A POSIÇÃO NO AFND
                
                if afnd[pos][0][0]: #ESTADO INICIAL AFND
                    afnd[pos][1].append(state)

                else: #ESTADO NÃO INICIAL AFND
                    afnd.append([(True,state),[state+1],tokens[token][char]])
                    state = state + 1
                

        else: #ESTADO NÃO INICIAL DO TOKEN
            
            afnd.append([(None,state),[state+1],tokens[token][char]])
            state = state + 1


        #ADICIONA ESTADO FINAL NO AFND
        if char == len(tokens[token])-1:
            afnd.append([(False,state),[None],None])
            state = state + 1

            
print("\nAFND\nTrue = Estado Inicial; False = Estado Final; None = Estado nem final nem inicial\n")
for state in range(0,len(afnd)):
    print(afnd[state])
