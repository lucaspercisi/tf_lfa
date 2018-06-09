def search_char(char):
    
    for i in range(0,len(afnd)):
        if char == afnd[i][2]:
            return True
    return False

def create_states():

    
    state = 0

    for token in range(0, len(tokens)):
        for char in range(0, len(tokens[token])):
                
            #se o char ainda não existe no afnd
            if not search_char(tokens[token][char]):

                if tokens[token][char] in first_chars_tokens:
                    afnd.append([0,[state+1],tokens[token][char]])
                else:
                    afnd.append([state,[state+1],tokens[token][char]])

                state = state + 1
                    
            #se o char já existe no afnd
            else:
                for i in range(0,len(afnd)):
                    if tokens[token][char] == afnd[i][2]:
                        afnd[i][1].append(state)
                        #afnd.append([state,[state+1],tokens[token][char]])
                        #state = state + 1
                    
                    
            #estado final do token
            if char == len(tokens[token])-1:
                afnd.append([state,[None],None])
                state = state + 1

             
    print('AFND: [ state [ next_state ] char ]\n(-> = Estado Inicial; ''*'' = Estado Final)\n')
    for i in range(0,len(afnd)):
        if afnd[i][0] == 0:
            print('  ',afnd[i])
        else:
            print('  ',afnd[i])
        
        
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
#tokens.sort()
print (tokens, 'TOKENS SEM O \\N\n')

#cria uma lista com a uniao dos caracteres dos tokens
chars_tokens = []
for i in range(0, len(tokens)):
    for j in range(0, len(tokens[i])):
        if tokens[i][j] not in chars_tokens:
            chars_tokens.append(tokens[i][j])
#chars_tokens.sort()
print (chars_tokens,'UNIAO DOS CARACTERS DOS TOKENS\n')

#cria lista contendo os caracteres iniciais de cada token
first_chars_tokens = []
for i in range(0, len(tokens)):
    first_chars_tokens.append(tokens[i][0])
print (first_chars_tokens,'CARACTERES INICIAIS\n')


afnd = []
create_states()
