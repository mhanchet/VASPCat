"""=== This file is part of VaspCat - <http://github.com/mcarl15/VaspCat> ===

Copyright 2015, Michael Carlson <mcarl15@ksu.edu>

VaspCat is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

VaspCat is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
VaspCat.  If not, see <http://www.gnu.org/licenses/>.

Module Description:
    Processes input files in order to save a new POSCAR output file.   
"""


import os
from vaspcat import cls,ExitError


def main(config,file,i,master,suffix):
    """Outputs POSCAR file using data from master dictionary.
    
    Args:
        config(ConfigParser): Contains settings specifying how the  
            outputted POSCAR file should be formatted.
        file(dict): Provides the path where the POSCAR file will be saved.
        i(int): Identifies which output group is having its POSCAR file saved.
        master(dict): Contains the basis vector and the atom names and
            coordinates which will go into the outputted file.
        suffix(str): Adds a suffix to the POSCAR file name if the user has
            chosen to do so or if multiple POSCAR files are being saved in the
            same working directory.
    """
    
    poscar = config['POSCAR']
    with open(os.path.join(file['output'][i],'POSCAR'+suffix), mode='w') as f:
        
        # Title
        title_mode = int(poscar['title_mode'])
        atom_set = sorted(set(master['atom']))
        f.write(get_title(atom_set,file,i,title_mode) + '\n')
        
        # Scaling constant
        f.write(' 1.00\n')

        # Lattice vectors
        lat_vec = [['{: 15.10f}'.format(position) for position in vector]
                   for vector in master['lat_vec']]
        lat_vec = [' '.join(vector) for vector in lat_vec]

        for vector in lat_vec:
            f.write(' ' + vector + '\n')

        # Atom symbol (optional)
        if poscar.getboolean('atom_label'):
            f.write(' ') 
            for name in atom_set:
                f.write('{:6} '.format(name))
            f.write('\n')

        # Atom count
        f.write(' ')
        
        for name in atom_set:
            f.write('{:<6} '.format(master['atom'].count(name)))
        f.write('\n')
        
        # Cell relaxation (optional)
        if poscar.getboolean('selective_dynamics'):
            f.write('Selective Dynamics\n')
            flag = 'F F F'
        else:
            flag = ''

        # Specify coordinates are fractional
        f.write('Direct\n')

        # Write fractional coordinates
        for atom in atom_set:
            for i,name in enumerate(master['atom']):
                if atom == name:
                    f.write('   {:12.10f} {:12.10f} {:12.10f} '.format(
                        master['x'][i],master['y'][i],master['z'][i]) + flag +
                        '\n')


def get_title(atom_set,file,i,title_mode):
    """Allows the user text for the first line of the output POSCAR file.
    
    Args:
        atom_set(list): Contains atomic symbols in alphabetic order.
        file(dict): Supplies the file name and output name for use as titles.
        i(int): Specifies which input file name should be grabbed.
        title_mode(int): Identifies what text should go on the first line
            of the POSCAR file output.  See config documentation for an
            explanation of each possible title.

    Raises:
        ExitError: Occurs if user chooses to stop VaspCat output before
            entering a custom title.

    Returns:
        Various strings depending on the value of title_mode.  See config
        documentation for an outline of the title possibilities.
    """
    
    if title_mode == 0:
        return file['name'][i]
        
    elif title_mode == 1:
        while True:
            print('What should the POSCAR title of ' + file['base'][i] + ' be?')
            title = input('>> ')[0:50]
            cls()

            if not title:
                print("POSCAR title for " + file['base'][i] + " " +
                      "cannot be blank.")
                print("Enter a new title, or type 'exit' " +
                      "to return to the menu.\n")
            elif title.lower() == 'exit':
                raise ExitError('POSCAR Error',
                        'User stopped VaspCat while providing ' +
                        'POSCAR titles.\n')
            else:
                return title
        
    elif title_mode == 2:
        return 'POSCAR'
    
    elif title_mode == 3:
        return ' '.join(atom_set)
    
    elif title_mode == 4:
        return file['base'][i]

