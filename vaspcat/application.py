"""=== This file is part of VaspCat - <http://github.com/mcarl15/VaspCat> ===

Copyright 2014, Michael Carlson <mcarl15@ksu.edu>

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
    Contains VaspCat program menu UI and file reading methods.   
"""

import configparser
import inspect
import os
import re
import sys

import pkg_resources as pkg

from vaspcat import ExitError,cls,output
from vaspcat.extend import filetype


def main():
    """Entry point into the VaspCat program.
    
    Returns:
        config: ConfigParser instance, containing values of every option
            set in the configuration file.  The settings control how the
            modules in VaspCat perform their functions.
        file: Dictionary sent to output.py once the user starts file output
            (by typing '0').  At the minimum, contains working directory.
            If [READER] section is found in config file, also contains
            paths, names, and extensions of read files.
    """
    
    cls()
    file = {'directory':os.getcwd()}
    config = load_settings(file['directory'])
    
    print('[VaspCat DFT Toolkit]') 
    print('Type the number of the option you wish to select.\n')
    
    tab = ''.ljust(2)
   
    menu_text = ('MAIN MENU\n'+
                 tab+'(0) Start file output\n'+
                 tab+'(1) Edit output settings\n'+
                 tab+'(2) Exit program\n')
    print(menu_text)
    
    # Main program loop.
    while True:
        choice = input('>> ')
    
        if choice == '0': # Start file output
            cls() 
            
            try:
                file = get_file(config,file)
                # output.main(config,file)
                print('Complete!','\n')

            except ExitError as exit:
                print(exit)
                
        elif choice == '1': # Edit output settings
            cls()
            print('TODO\n')

        elif choice == '2': # Exit program
            cls()
            print('Exiting VaspCat...')
            sys.exit()
        
        else:
            cls()
        
        print(menu_text)


def load_settings(directory,user_file=True) -> 'ConfigParser object':
    """Reads default and user config settings from external files.
    
    Args:
        directory: String containing the directory VaspCat is started in.
            This is the search path for user config.ini files.
        user_file: Optional parameter specifying if the method should 
            attempt to find user config files in directory.
            (default=True)

    Returns:
        config: A ConfigParser object containing the sections and options
            specifying VaspCat behavior.
    """
 
    print('Loading VaspCat settings...')
    config = configparser.ConfigParser()

    # Load default config settings from file.  Uses pkg_resource module.
    default_config = pkg.resource_filename(
            'vaspcat','config.ini')
    
    with open(default_config, 'r') as default:
        config.read_file(default)
    
    # If requested, try to find user config settings in directory.
    if user_file:
        if config.read(os.path.join(directory,'config.ini')):
            print('User settings loaded from ' + directory + '.\n')
        else:
            print('No user settings found in ' + directory + '.')
            print('VaspCat default settings loaded.\n')
    else:
        print('VaspCat default settings loaded.\n')

    return config


def get_file(config,file) -> 'File_dictionary':
    """Populates keys of file dictionary based on READER config settings.

    Args:
        config: ConfigParser object with program settings.  Used in method to
            determine how input files should be treated.
        file: Dictionary with keys having file names, paths, and extensions.

    Returns:
        file: Updated dictionary with the complete set of file information 
            output.py needs to work properly.
    """

    reader = config['READER']
    
    if reader['file_type_read'].lower() != 'none': 
        print('Scanning ' + file['directory'] + ' for supported files...\n')
        file = scan_dir(reader,file)  
    else:
        if reader.getboolean('name_prompt'):
            
            while True:    
                print('What should the output name be known as?')
                test_name = input('>> ')
                cls()
                
                test_name = name_settings([],test_name)
                
                if test_name:
                    file['name'] = [test_name]
                    break
        else:
            file['name'] = ['output']
    
    return file
    

def scan_dir(reader,file) -> 'File dictionary': 
    """Finds files with supported extensions from current working directory.
    
    Args:
        reader: ConfigParser object with settings pertaining to file reading.
        file: Dictionary to be populated with paths, names, and extensions
            of supported files in working directory.
    
    Exceptions:
        ExitError: Thrown if no supported files were found in the working
            directory, even though the user asserted otherwise in the
            program settings.

    Returns: 
        file: Dictionary with keys 'path', 'name', 'extension', and 'directory'
            giving locations and extensions of supported files.
    """
    
    # Get list of extensions the user wants read from the working directory,
    # and determine if VaspCat supports them.
    requested = reader['file_type_read'].lower().split()
    supported = [name.lower() 
                 for name, obj in inspect.getmembers(filetype)
                 if inspect.isclass(obj)]

    if 'all' in requested:
        match = supported

    else:
        match = [ext for ext in requested 
                 if ext in supported]
        
    # Get supported files by splitting extensions from scanned files in 
    # working directory.
    file_info = [(f,ext) for ext in match
                 for f in os.listdir(file['directory'])
                 if os.path.isfile(f) 
                 if ext in os.path.splitext(f)[1].lower()]
    
    file_name = [data[0] for data in file_info]
    extension = [data[1] for data in file_info]
    
    # Get supported files which do not have extensions (such as POSCAR)
    # by looking for the file type plus, optionally, an underscore at 
    # the start of the file name.
    file_info = [(f,ext) for ext in match
                 for f in os.listdir(file['directory'])
                 if os.path.isfile(f)
                 if re.search(re.compile("(?i)^"+ext+"_*"),f)
                 if f not in file_name]
    
    file_name.extend([data[0] for data in file_info])
    extension.extend([data[1] for data in file_info])
    
    if not file_name:
        cls()
        
        if not match:
            match = 'None'
        else:
            match = ', '.join(match)
        
        raise ExitError('READER Error',
            'Readable files not found in {0}.'.format(file['directory']),
            'Choose a directory with supported files, or ' +
            'modify the file_type_read',
            'option in the config file.\n',
            'File formats read: ' + match,
            'File formats supported: ' + ', '.join(supported) + '\n')

    # Extract name from file_name, or have user provide the file name,
    # depending on the value of name_prompt in VaspCat settings.
    name_lst = []
    
    if reader.getboolean('name_prompt'): 
        for name in file_name:
            extra = 'for the file {0} '.format(name)
            
            while True:
                print('What should the file {0} be known as?'.format(name))
                test_name = input('>> ')
                cls()

                test_name = name_settings(name_lst,test_name,extra)
                    
                if test_name:
                    name_lst.append(test_name)
                    break

    else:
        extract = [os.path.splitext(f)[0] for f in file_name]
        
        # If extension is at the start of the file name, remove it.
        for i,name in enumerate(extract):
            extract[i] = re.sub("(?i)^" + extension[i] + "_*",'',extract[i])
        
        for i,name in enumerate(extract):
            
            extra = 'for the file {0} '.format(file_name[i])    
            
            if extract.count(name) > 1:
                name_lst.append(name + '_' + extension[i])
            elif not name:
                print('Extracted name for {0} ' +
                      'is blank.\n'.format(file_name[i]))
                
                while True:
                    print('What should the file {0} ' +
                          'be known as?'.format(file_name[i]))
                    test_name = input('>> ')
                    cls()
                    
                    test_name = name_settings(name_lst,test_name,extra)
                    
                    if test_name:
                        name_lst.append(test_name)
                        break
            else:
                name_lst.append(name)
    
    file['path'] = [os.path.join(file['directory'],base)
                    for base in file_name]
    file['name'] = name_lst          
    file['extension'] = extension
    
    return file


def name_settings(name_lst,test_name,extra='') -> 'test_name or blank string':
    """Test if proposed output names are duplicates or blank.

    Args:
        name_lst: List containing the names that have already been extracted.
        test_name: Proposed output name for addition to name_lst.
        extra: String added to error message specifying its context.
            (default = '')

    Returns:
        test_name: Returns blank string if an error is found, or parsed name
            if it is not blank or a duplicate.
    
    Raises:
        ExitError: Exception raised if user wishes to return to VaspCat menu
            instead of providing a new output name.
    """
    
    # Remove characters that are not dashes or alphanumeric from output name.
    test_name = re.sub("[^\w-]*",'',test_name)[0:50] 
    
    # Return a blank string or raise an exception for errors
    if test_name in name_lst:   # test_name is duplicate
        print("Output name " + extra + "already exists.")
        print("Provide a new name, or type 'exit' to return to the menu.\n")
        print("Duplicate name: " + test_name + "\n")

        return ''

    elif not test_name:  # test_name is blank
        print("Output name " + extra + "cannot be blank.")
        print("Provide a new name, or type 'exit' to return to the menu.\n")

        return ''

    elif test_name.lower() == 'exit':  # User wants to return to menu
        raise ExitError('Name Error',
            'User stopped VaspCat while providing output file names.\n')
    
    else:  # test_name is valid
        return test_name

