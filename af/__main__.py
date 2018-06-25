import os
from .inputfile import Constructor


def main():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    file_path = os.path.join(dir_path, 'tokens_GRs.txt')

    af = Constructor(file_path)
    af.fill_afnd()
    af.print_afnd()
    af.print_afd()

    contin = 'S'

    while contin == 'S':
        # token = str(input('Digite o token a ser verificado: '))
        # verificar token

        contin = str(input('Deseja continuar? S/N: ')).upper()

    print('Saindo...')


main()
