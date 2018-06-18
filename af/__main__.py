import os
from .inputfile import Constructor


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
file_path = os.path.join(dir_path, 'tokens_GRs.txt')

afnd = dict()
constructor = Constructor(afnd, file_path)
constructor.fill_afnd()
constructor.print()
