import inspect
import os
import sys
from vaspcat.extend import filetype


def main(master,config):
    '''Outputs POSCAR file using data from master dictionary.'''
   
    atom_list = poscar.output(directory)

    print('COMPLETE!','\n')
    return atom_list

    
    def output(self,directory) -> 'Atom list with same order as POSCAR':
        '''Saves POSCAR file in directory

        Args:
            directory: Specifies where the POSCAR file should be saved.

        Returns:
            List of atoms having the same order as the output POSCAR file.
            This information is found from element 0 in atom_info, a list
            having the following form:

            [[atom 1 name, # of atom 1], [atom 2 name, # of atom 2], ...]
        '''
        
        lat_vec, atom_info, frac_pos = self.parse(self.read(self.path))
 
        with open(os.path.join(directory, 'POSCAR'), mode='w') as f:
            #Line 1: System Name
            f.write('POSCAR\n') 

            #Line 2: Scaling Constant
            f.write('1.00'.rjust(7) + '\n')

            #Line 3: Lattice Vectors
            for line in lat_vec:
                f.write(' ' + line + '\n')

            #Line 4: Atoms per Species
            atom_count = ' '.join([str(count[1]) for count in atom_info])
            f.write(''.rjust(3))
            f.write(' '.join([atom[0] for atom in atom_info]) + '\n')
            f.write(''.rjust(3) + atom_count + '\n')

            #Lines 5/6: Allow cell relaxation and specify direct coordinates
            f.write('Selective Dynamics\nDirect\n')

            #Lines 7-End: Cell Coordinates
            for line in frac_pos:
                f.write(' ' + line + ' F F F\n')

        return [atom[0] for atom in atom_info]  












        





         

    
    
                



    








    
