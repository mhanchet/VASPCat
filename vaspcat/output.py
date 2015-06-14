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
    Calls methods that add output files to newly created directories.
"""


import configparser
import re
import os

from vaspcat import cls,ExitError
from vaspcat.core import incar,kpoints,poscar,potcar
from vaspcat.extend import filetype


def main(config,file):
    """Set up output directories and call output methods based on settings.
    
    Args:
        config(ConfigParser): Settings object containing OUTPUT section 
            specifying what new directories and file types should be created.
        file(dict): Has keys 'base', 'directory', 'extension', and 'name' 
            used in other conversion modules.  If 'extension' is an empty list,
            modules like poscar.py required a file input will be skipped.
    
    Returns:
        String with message indicating successful file output.
    """

    print('Setting up output directory names...\n')
    output = config['OUTPUT']
    
    if output.getboolean('folder_output'):
        file['output'] = create_directory(file,output)
    else:
        file['output'] = [file['directory'] for i in range(len(file['name']))] 
        cls()

    print('Saving output files...\n')
    for i,path in enumerate(file['output']):

        if file.get('extension'):
            file_path = os.path.join(file['directory'],file['base'][i])
            
            # Create object from filetype.py classes to parse input files.
            extension = file['extension'][i].capitalize()
            file_class = getattr(filetype,extension)
            file_obj = file_class(file_path)
            master = file_obj.get()
        else:
            master = {}
        
        # Determine if new files should have output name suffixes.
        # If folder_output is false, suffixes must be used.
        if output.getboolean('folder_output'):
            
            if output.getboolean('name_as_suffix'):
                suffix = '_' + file['name'][i]
            else:
                suffix = ''
        else:
            suffix = '_' + file['name'][i]
        
        # Output files that have a dependence on file input.
        if master:
            if output.getboolean('POSCAR'):
                poscar.main(config,file,i,master,suffix)
            if output.getboolean('POTCAR'):
                potcar.main(config,file,i,master,suffix)

        if output.getboolean('INCAR'):
            incar.main(config,file,i,suffix)
        if output.getboolean('KPOINTS'):
            kpoints.main(config,file,i,suffix)
    cls()
    return 'Output complete!\n'
   

def create_directory(file,output):
    """Creates new directories for storing output files created by program.
    
    Args: 
        file(dict): Stores the paths of the folders where output files
            will be saved to.
        output(ConfigParser): Specifies if user must enter
            a directory name manually for each set of file conversions.
    
    Raises:
        PermissionError OR SyntaxError: Raised when the requested new folder 
            name has an improper format.  The user is asked
            to enter a new directory name.
        FileExistsError: Raised if the folder requested for creation exists.
            The program continues execution in this case.

    Returns:
        file(dict): The key 'output' has been updated with the full paths of
            the folders where output files will be saved
    """

    if output.getboolean('folder_prompt'):
        dir_list = []

        if file.get('base'):
            for name in file['base']:  
                extra = 'for {0} '.format(name)

                while True:
                    print('What should the output directory ' + extra + 
                          'be known as?')
                    test_dir = input('>> ')
                    cls()

                    test_dir = directory_check(dir_list,test_dir,extra)

                    if test_dir:
                        dir_list.append(test_dir)
                        break
        else:
            extra = ''

            while True:
                print('What should the output directory be known as?')
                test_dir = input('>> ')
                cls()

                test_dir = directory_check(dir_list,test_dir)

                if test_dir:
                    dir_list.append(test_dir)
                    break
    else:
        dir_list = file['name']
        cls()

    print('Saving output directories...')
    file['output'] = [os.path.join(file['directory'],name)
                      for name in dir_list]

    for path in file['output']:
        try:
            os.makedirs(path)            
        except FileExistsError:
            continue
    cls()
    return file['output']

        
def directory_check(dir_list,test_dir,extra=''):
    """Stops the user from writing two sets of inputs to one output folder.
    
    Args:
        dir_list(list): Contains names of folders that are already being 
            used as output destinations.
        test_dir(str): Name of the folder the user has chosen for saving.
        extra(str): Optional text telling the user what input file is 
            associated with the desired output directory. (default = '')

    Raises:
        ExitError: Occurs if user exits the program instead of specifying
            an output directory name.

    Returns:
        if (not test_dir) or (test_dir not in dir_list):
            Blank string indicating a new directory name is needed.
        else:
            test_dir(str): Parsed and validated directory name.
    """

    test_dir = re.sub("[^\w-]*",'',test_dir)[0:50]

    if test_dir in dir_list:
        print("Output directory name " + extra + "already used.")
        print("Provide a new name, or type 'exit' to return to the menu.\n")
        print("Duplicate name: " + test_dir + "\n") 

        return ''

    elif not test_dir:
        print("Output directory name " + extra + "cannot be blank.")
        print("Provide a new name, or type 'exit' to return to the menu.\n")

        return ''

    elif test_dir.lower() == 'exit':
        raise ExitError('Name Error',
                'User stopped VaspCat while ' + 
                'providing output directory names.\n')

    else:
        return test_dir

