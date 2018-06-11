#adiciona os tokens do arquivo em uma lista
tokens = []
f = open('tokens_GRs.txt','r')
for line in f:
    tokens.append(line)
f.close()
print (tokens,'TOKENS')

#remove os '\n' dos tokens
for i, token in enumerate(tokens):
    pos = token.find('\n')
    if pos > -1:
        token = token[:pos]
    tokens[i] = token

#cria uma lista com a uniao dos caracteres dos tokens
chars_tokens = []
for i in range(0, len(tokens)):
    for j in range(0, len(tokens[i])):
        if tokens[i][j] not in chars_tokens:
            chars_tokens.append(tokens[i][j])

#cria lista contendo os caracteres iniciais de cada token
first_chars_tokens = []
for i in range(0, len(tokens)):
    first_chars_tokens.append(tokens[i][0])

print (tokens,'TOKENS')
print (chars_tokens,'UNIAO DOS CARACTERS DOS TOKENS\n')
print (first_chars_tokens,'CARACTERES INICIAIS\n')


afnd = []

def addedChar_afnd(char):

    for state in range(0,len(afnd)):
        if afnd[state][2] == char:
            return True
    return False

def bucaPosChar_afnd(char):

    for state in range(0,len(afnd)):
        if afnd[state][2] == char:
            if afnd[state][0][0]:
                return state
    return -1

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
                    afnd[pos][1].append(state+1)

                else: #ESTADO NÃO INICIAL AFND
                    afnd.append([(True,state),[state+1],tokens[token][char]])

                state = state + 1
                

        else: #ESTADO NÃO FINAL

            #if not addedChar_afnd(tokens[token][char]):#NÃO FOI ADICIONADO
            afnd.append([(None,state),[state+1],tokens[token][char]])
            state = state + 1

        #ADICIONA ESTADO FINAL
        if char == len(tokens[token])-1:
            afnd.append([(False,state),[None],None])
            state = state + 1

            
print("True = Estado Inicial; False = Estado Final; None = Estado não final nem inicial\n")
for state in range(0,len(afnd)):
    print(afnd[state])
print('\n')
for state in range(0,len(afnd)):
    if afnd[state][0][0]:
        print(afnd[state])
