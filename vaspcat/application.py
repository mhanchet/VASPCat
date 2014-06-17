import os
from vaspcat.src import poscar, potcar  

def main():
    directory = os.getcwd()
    print('VaspCat')
    atom_list = poscar.main(directory)
    potcar.main(directory, atom_list)
    print('Done!')
    
