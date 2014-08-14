import inspect
import os
import re

import pkg_resources as pkg

from vaspcat import cls,ExitError
from vaspcat.extend import filetype

def main(config,file) -> 'File_dictionary':
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
        file = scan_directory(reader,file)  
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
            cls() 
    
    return file
    

def scan_directory(reader,file) -> 'File dictionary': 
    """Finds files with supported extensions from current working directory.
    
    Args:
        reader: ConfigParser object with settings pertaining to file reading.
        file: Dictionary to be populated with paths, names, and extensions
            of supported files in working directory.
    
    Raises:
        ExitError: Thrown if no supported files were found in the working
            directory, even though the user asserted otherwise in the
            program settings.

    Returns: 
        file: Dictionary with keys 'directory', 'base', 'extension', and 'name'
            giving required information to locate and identify readable files.
    """
    
    # Get list of extensions the user wants read from the working directory,
    # and determine if VaspCat supports them.
    requested = reader['file_type_read'].lower().split()
    supported = [name.lower() 
                 for name,obj in inspect.getmembers(filetype)
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
            'Readable files not found in ' +
            '{0} directory.'.format(os.path.basename(file['directory'])),
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
            extra = 'for {0} '.format(name)
            
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
    
    file['base'] = file_name
    file['name'] = name_lst          
    file['extension'] = extension
    
    cls()
    return file


def name_settings(name_lst,test_name,extra='') -> 'test_name or blank string':
    """Test if proposed output names are duplicates or blank.

    Args:
        name_lst: List containing the names that have already been extracted.
        test_name: Proposed output name for addition to name_lst.
        extra: String added to error message specifying its context.
            (default = '')

    Returns:
        test_name: Returns empty string if name is blank or a duplicate, 
            or parsed name otherwise.
    
    Raises:
        ExitError: Exception raised if user wishes to return to VaspCat menu
            instead of providing a new output name.
    """
    
    # Remove characters that are not dashes or alphanumeric from output name.
    test_name = re.sub("[^\w-]*",'',test_name)[0:50] 
    
    if test_name in name_lst:   
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

