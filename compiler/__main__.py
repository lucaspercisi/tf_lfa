import os
import pickle
from compiler.lexical import Constructor
from compiler.sintax import LALR

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
file_path = os.path.join(dir_path, 'inputs')

# AUTÔMATO FINITO
constructor = Constructor()

constructor.fill_afnd()  # preenche o AFND com os dados do arquivo de entrada
constructor.remove_epsilon()  # remove os EPSILON transições
constructor.afnd_determinization()  # determiniza o afnd
constructor.remove_dead()  # remove os estados mortos
constructor.remove_unreachable()  # remove os estados inatingíveis
# constructor.print_afd()  # imprime o AFD finalizado

# carrega os objetos em arquivos para congelá-los
# with open(os.path.join(file_path, 'afd.object'), 'wb') as afd_object_file:
#     pickle.dump(constructor.afd, afd_object_file)
# with open(os.path.join(file_path, 'alpha.object'), 'wb') as alpha_object_file:
#     pickle.dump(constructor.alphabet, alpha_object_file)

# lê os objetos dos arquivos
with open(os.path.join(file_path, 'afd.object'), 'rb') as afd_object_file:
    constructor.afd = pickle.load(afd_object_file)
with open(os.path.join(file_path, 'alpha.object'), 'rb') as alpha_object_file:
    constructor.alphabet = pickle.load(alpha_object_file)

# recognizing_test_tokens = ['int', 'float', 'void', 'char', 'return', 'if', 'while', 'else', 'for', 'do', 'break', 'continue', 'switch', 'case', 'default', '<', '>', ':', '(', ')', '=', '==', '<=', '>=', '!=', '{', '}', '[', ']', ';', '+', '-', '*', '/', ', ', '+=', '-=', '*=', '/=', '^=', '&=', '|=', '?', '||', '&&', '>>', '<<', '%', '|', '^', '&', '!', '~', '++', '--', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'variavel_', '1', '88', '564', '-120', '-5.18', '0.0', '1000.0000037']
#
# afd_finals = []
# recognizing_finals = []
#
# for key, line in constructor.afd.items():
#     if line.final:
#         afd_finals.append(key)
#
# for token in recognizing_test_tokens:
#     # print('\nReconhecendo token [ {} ]'.format(token))
#     recognized, state, message = constructor.token_recognition(token)
#     # print(recognized, state, message)
#     if recognized and state not in recognizing_finals:
#         print(state, ':', ', #', token)
#         recognizing_finals.append(state)
#     elif not recognized:
#         print(recognized, state, message)
#
# print('Estados não reconhecidos')
# print(set(afd_finals)-set(recognizing_finals))

#  TABELA DE SÍMBOLOS
constructor.build_separators()  # Constroí as listas contendo os separadores da linguagem.
constructor.clean_source_code()  # Limpa o código-fonte para construção da self.ts.
constructor.build_symbol_table()  # Constrói a Tabela de Símbolos de acordo com o AF
# constructor.show_symbol_table()  # Mostra Tabela de Símbolos

# Analisador sintático LALR
lalr = LALR(st=constructor.st)
lalr.load()
lalr.analyze()
