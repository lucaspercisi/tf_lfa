#adiciona os tokens do arquivo em uma lista
tokens = []
f = open('tokens_GRs.txt','r')
for line in f:
    tokens.append(line)
f.close()
print (tokens,'TOKENS DO ARQUIVO\n')

#remove os '\n' dos tokens
for i, token in enumerate(tokens):
    pos = token.find('\n')
    if pos > -1:
        token = token[:pos]
    tokens[i] = token

#cria uma lista com a uniao dos caracteres dos tokens
alphabet = []
for i in range(0, len(tokens)):
    for j in range(0, len(tokens[i])):
        if tokens[i][j] not in alphabet:
            alphabet.append(tokens[i][j])

print (tokens,'TOKENS TRATADOS\n')
print (alphabet,'ALFABETO\n')

afnd = dict()

def addedChar_afnd(char):
    
    for i in range(0,len(afnd)):
        if char in afnd[i]:
            return True

    return False


def bucaPosChar_afnd(char):

    for state in range(0,len(afnd)):
        if char in afnd[state]:
            if afnd[state][char][1]:
                return state
    return -1


state = 0
for token in range(0, len(tokens)):
    for char in range(0, len(tokens[token])):

        symbol = tokens[token][char]
        
        if char == 0: #ESTADO INICIAL TOKEN
            
            if not addedChar_afnd(symbol):#NÃO FOI ADICIONADO
                afnd.update({state:{symbol:[[state+1], True]}}) #TRUE
                state = state + 1

            else:#JÁ FOI ADICIONADO
                
                key = bucaPosChar_afnd(symbol) #ENCONTRA A POSIÇÃO NO AFND

                if key >= 0: #ESTADO INICIAL AFND
                    afnd[key][symbol][0].append(state) #TRUE

                else: #ESTADO NÃO INICIAL AFND
                    afnd.update({state:{symbol:[[state+1], True]}})
                    state = state + 1

        else: #ESTADO NÃO FINAL
            afnd.update({state:{symbol:[[state+1], None]}})
            state = state + 1

        #ADICIONA ESTADO FINAL
        if char == len(tokens[token])-1:
            #afnd.append([(False,state),[None],None])
            afnd.update({state:{None:[[None], False]}})#FALSE

            state = state + 1

print("\nTrue = Estado Inicial; False = Estado Final; None = Estado não final nem inicial\n")
for state in range(0,len(afnd)):
    print(state,':',afnd[state])

print ("\nDETERMINIZAÇÃO:\n")

