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
    Reads user variable specifications to save a new INCAR file.   
"""


import configparser
import os

from vaspcat import cls,ExitError


def main(config,file,i,suffix):
    """Outputs INCAR file using data from config settings.
    
    Args:
        config(ConfigParser): Contains settings specifying how variables will
            be saved in the INCAR file output.
        file(dict): Provides the path where the INCAR file will be saved.
        i(int): Identifies which output group is having its INCAR file saved.
        suffix(str): Adds a suffix to the INCAR file name if the user has
            chosen to do so or if multiple INCAR files are being saved in the
            same working directory.
    """

    incar = config['INCAR']
    
    with open(os.path.join(file['output'][i],'INCAR'+suffix), mode='w') as f:
        
        if incar['system'].lower() != 'off':
            title_mode = int(incar['system'])
            f.write('SYSTEM = ' + get_title(file,i,title_mode)+'\n\n')

        output = [key.upper() + ' = ' + get_bool(incar[key]) + '\n' 
                  for key in sorted(incar)
                  if key != 'system' if incar[key].lower() != 'off']
        
        for text in output:
            f.write(text)


def get_title(file,i,title_mode):
    """Returns a title for the 'SYSTEM' tag of the INCAR file.

    Args:
        file(str): Tells the user what output group they are giving a title.
        i(int): Identifies which output group is having its INCAR file saved.
        title_mode(int): Identifies what text should go in the 'SYSTEM' tag
            output of the INCAR file.  See config documentation for an
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
            print('What should the INCAR title of ' + file['name'][i] + ' be?')
            title = input('>> ')[0:50]
            cls()

            if not title:
                print("INCAR title for " + file['name'][i] + " " +
                      "cannot be blank.")
                print("Enter a new title, or type 'exit' " +
                      "to return to the menu.\n")
            elif title.lower() == 'exit':
                raise ExitError('INCAR Error',
                        'User stopped VaspCat while providing ' +
                        'INCAR titles.\n')
            else:
                return title
    
    elif title_mode == 2:
        return 'INCAR'


def get_bool(value):
    """Modifies boolean config values to meet INCAR format requirements.

    Args:
        value(str): Text of a particular option in VaspCat settings.

    Returns:
        Different strings depending on whether or not the value supplied
        to the function is a boolean.
    """

    if value.lower() == 'true':
        return '.TRUE.'
    elif value == 'false':
            return '.FALSE.'
    else:
        return value

