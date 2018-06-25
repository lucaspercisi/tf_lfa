import os
from .inputfile import Constructor


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
file_path = os.path.join(dir_path, 'tokens_GRs.txt')

af = Constructor(file_path)
af.fill_afnd()
af.print_afnd()
af.print_afd()
