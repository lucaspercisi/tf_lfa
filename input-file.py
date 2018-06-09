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

#return [token, char_tokens, first_char_tokens]
