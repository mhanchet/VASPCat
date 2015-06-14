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
    Processes input files in order to save a new POTCAR output file.   
"""


import os

from vaspcat import ExitError


def main(config,file,i,master,suffix):
    """Concatinates atomic POTCAR files into an output POTCAR file.
    
    Args:
        config(ConfigParser): Contains settings specifying the directory 
            where atomic POTCAR files are stored.
        file(dict): Provides the path where the POTCAR file will be saved.
        i(int): Identifies which output group is having its POTCAR file saved.
        master(dict): Contains the input atomic symbols that identify 
            the POTCAR files to concatinate.
        suffix(str): Adds a suffix to the POTCAR file name if the user has
            chosen to do so or if multiple POTCAR files are being saved in the
            same working directory.
    
    Raises:
        ExitError: Occurs if a POTCAR file for a required atom can't be found.
    """
    
    potcar = config['POTCAR']
    atom_set = sorted(set(master['atom']))
    directory = os.path.expandvars(potcar['path'])
    path = []

    for atom in atom_set:
        in_file = os.path.join(directory,atom,'POTCAR')
        path.append(in_file)
     
    atom_lst = []
    for in_file,atom in zip(path,atom_set):
        if not os.path.isfile(in_file):
            atom_lst.append(atom)
    
    if len(atom_lst) > 0:
        atom_str = ', '.join(atom_lst)
        raise ExitError('POTCAR Error', 'Required POTCAR files were not ' +
                        'found in ' + os.path.basename(directory) + '.',
                        'Add the missing files, and run VaspCat again.\n',
                        'Missing atoms: {0}\n'.format(atom_str))
    else:
        out_file = os.path.join(file['output'][i],'POTCAR'+suffix)
        with open(out_file,'a') as fout:
            for in_file,atom in zip(path,atom_set):
                with open(in_file,'r') as fin:
                    for line in fin:
                        fout.write(line)   
        
