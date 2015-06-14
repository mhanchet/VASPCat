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
    Saves paths and extensions of parsable files to the dictionary 'file'.   
"""


import inspect
import os
import re

from vaspcat import cls,ExitError
from vaspcat.extend import configuration,filetype


def main(config,file):
    """Populates keys of 'file' dictionary based on READER config settings.

    Args:
        config(ConfigParser): Contains program settings obtained from
            settings.py.  These settings determine what file types are read
            and what name the program uses to identify a particular set
            of output operations.
        file(dict): Object provided with file names, paths, and extensions
            supported by VaspCat.

    Returns:
        file(dict): Complete set of information output.py needs to locate
            and process input files.
    """

    reader = config['READER']
    
    if reader['file_type_read'].lower() != 'none': 
        print('Scanning ' + file['directory'] + ' for supported files...\n')
        file = scan_directory(file,reader)  
    else:
        if reader.getboolean('name_prompt'):
            
            while True:    
                print('What should the output name be known as?')
                test_name = input('>> ')
                cls()
                
                test_name = name_check([],test_name)
                
                if test_name:
                    file['name'] = [test_name]
                    break
        else:
            file['name'] = ['output']
            cls() 
    
    return file
    

def scan_directory(file,reader): 
    """Finds files with supported extensions from current working directory.
    
    Args:
        file(dict): Populated here with paths, names, and extensions
            of supported files in working directory.
        reader(ConfigParser): Subset of 'config' ConfigParser object with 
            settings only related to file reading.
            
    Raises:
        ExitError: Thrown if no supported files were found in the working
            directory, even though the user specified otherwise in the
            program settings.  Program returns to main menu.

    Returns: 
        file(dict): Provides the keys 'directory', 'base', 'extension', 
            and 'name' required for locating and identifying readable files. 
    """
    
    requested = reader['file_type_read'].lower().split()
    supported = configuration.items(setting=False)

    if 'all' in requested:
        match = supported
    else:
        match = [extension for extension in requested 
                 if extension in supported]
        
    # The list of tuples 'file_info' contains the name of the supported file
    # in index 0 and its extension in index 1.
    file_info = [(f,extension) for extension in match
                 for f in os.listdir(file['directory'])
                 if os.path.isfile(f) 
                 if extension in os.path.splitext(f)[1].lower()]
    
    file_name = [data[0] for data in file_info]
    extension = [data[1] for data in file_info]
    
    if not file_name:
        cls()
        
        if not match:
            match = 'None'
        else:
            match = ', '.join(match)
        
        raise ExitError('READER Error',
            'Readable files not found in ' +
            '{0} directory.'.format(os.path.basename(file['directory'])),
            'Choose a directory with supported files, or ' +
            'modify the file_type_read',
            'option in the config file.\n',
            'Options read: ' + match,
            'Options supported: ' + ', '.join(supported) + '\n')

    # Extract name from 'file_name', or have user provide the file name,
    # depending on the value of 'name_prompt' in VaspCat settings.
    name_list = []
    
    if reader.getboolean('name_prompt'): 
        for name in file_name:
            extra = 'for {0} '.format(name)
            
            while True:
                print('What should the file {0} be known as?'.format(name))
                test_name = input('>> ')
                cls()

                test_name = name_check(name_list,test_name,extra)
                    
                if test_name:
                    name_list.append(test_name)
                    break
    else:
        extract = [os.path.splitext(f)[0] for f in file_name]
        
        
        for i,name in enumerate(extract):
            extra = 'for the file {0} '.format(file_name[i])    
            
            if extract.count(name) > 1:
                name_list.append(name + '_' + extension[i])
            elif not name:
                print('Extracted name for {0} ' +
                      'is blank.\n'.format(file_name[i]))
                
                while True:
                    print('What should the file {0} ' +
                          'be known as?'.format(file_name[i]))
                    test_name = input('>> ')
                    cls()
                    
                    test_name = name_check(name_list,test_name,extra)
                    
                    if test_name:
                        name_list.append(test_name)
                        break
            else:
                name_list.append(name)
    
    file['base'] = file_name
    file['name'] = name_list          
    file['extension'] = extension
    cls()
    return file


def name_check(name_list,test_name,extra=''):
    """Test if proposed output names are duplicates or blank.

    Args:
        name_list(list): Names that have already been extracted.
        test_name(list): Proposed output name for addition to 'name_list'.
        extra(str): Text added to error message specifying its context.
            (default = '')

    Raises:
        ExitError: Exception raised if user wishes to return to VaspCat menu
            instead of providing a new output name.
 
    Returns:
        if (not test_name) or (test_name not in name_list):
            Blank string indicating a new output name is needed.
        else:
            test_name(str): Parsed and validated output name.
    """
    
    # Remove characters that are not dashes or alphanumeric from output name.
    test_name = re.sub("[^\w-]*",'',test_name)[0:50] 
    
    if test_name in name_list:   
        print("Output name " + extra + "already used.")
        print("Provide a new name, or type 'exit' to return to the menu.\n")
        print("Duplicate name: " + test_name + "\n")
        return ''

    elif not test_name:  
        print("Output name " + extra + "cannot be blank.")
        print("Provide a new name, or type 'exit' to return to the menu.\n")
        return ''

    elif test_name.lower() == 'exit':  
        raise ExitError('Name Error',
            'User stopped VaspCat while providing output file names.\n')
    
    else:  
        return test_name

