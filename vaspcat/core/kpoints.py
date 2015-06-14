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
    Reads user variable specifications to save a new KPOINTS file.   
"""


import configparser
import os

from vaspcat import cls,ExitError


def main(config,file,i,suffix):
    """Outputs KPOINTS file using data from config settings.
    
    Args:
        config(ConfigParser): Contains settings specifying how variables will
            be saved in the KPOINTS file output.
        file(dict): Provides the path where the KPOINTS file will be saved.
        i(int): Identifies which output group is having its KPOINTS file saved.
        suffix(str): Adds a suffix to the KPOINTS file name if the user has
            chosen to do so or if multiple KPOINTS files are being saved in the
            same working directory.
    """

    kpoints = config['KPOINTS']

    with open(os.path.join(file['output'][i],'KPOINTS'+suffix), mode='w') as f:
        
        # Section 1: Comment line
        title_mode = int(kpoints['title_mode'])
        f.write(get_title(file,i,title_mode) + '\n')

        # Section 2: Number of KPOINTS
        f.write(kpoints['point_mode'] + '\n')

        # Section 3: Mesh specification line
        mode = int(kpoints['point_mode'])
        
        # Section 4: Coordinate data
        if mode == 0:
            f.write('Monkhorst-Pack\n')
            for var in ('x','y','z'):
                f.write(kpoints['mesh_' + var] + ' ')
            f.write('\n0 0 0')
        
        elif mode == 1:
            f.write('Reciprocal\n')
            f.write('0 0 0 1\n')


def get_title(file,i,title_mode):
    """Returns a title for the first line of the KPOINTS file.

    Args:
        file(str): Tells the user what output group they are giving a title.
        i(int): Identifies which output group is having its KPOINTS file saved.
        title_mode(int): Identifies what text should go in the first line 
            of the output KPOINTS file.  See config documentation for an
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
            print('What should the KPOINTS title of ' + file['name'][i] + 
                    ' be?')
            title = input('>> ')[0:50]
            cls()

            if not title:
                print("KPOINTS title for " + file['name'][i] + " " +
                      "cannot be blank.")
                print("Enter a new title, or type 'exit' " +
                      "to return to the menu.\n")
            elif title.lower() == 'exit':
                raise ExitError('KPOINTS Error',
                        'User stopped VaspCat while providing ' +
                        'KPOINTS titles.\n')
            else:
                return title
    
    elif title_mode == 2:
        return 'KPOINTS'

