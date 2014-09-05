import configparser
import re
import os

from vaspcat import ExitError,cls
from vaspcat.core import incar,kpoints,poscar,potcar
from vaspcat.extend import filetype


def main(config,file):
    '''Set up output directories and call output methods based on settings.
    
    Args:
        config: ConfigParser instance, containing OUTPUT section specifying
            what new directories and file types should be created.
        file: Dictionary containing keys for 'base', 'name', 'directory',
            and 'extension' to be used in other conversion modules.  
            If these items are empty, modules like poscar.py requiring a file 
            input will be skipped.   
    '''

    print('Setting up output directory names...\n')
    output = config['OUTPUT']
    
    if output.getboolean('folder_output'):
        file['output'] = create_directory(output,file)
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
                poscar.main(master,config,file,suffix,i)
            if output.getboolean('POTCAR'):
                potcar.main(master,config,file,suffix,i)

        if output.getboolean('INCAR'):
            incar.main(config,file,suffix,i)
        if output.getboolean('KPOINTS'):
            kpoints.main(config,file,suffix,i)
    cls()
   

def create_directory(output,file):
    '''Creates output directory for file conversion operations if requested.
    
    Args: 
        output: ConfigParser section instance, specifying if user must enter
            a directory name manually for each set of file conversions.
    
    Raises:
        PermissionError OR SyntaxError: Raised when the requested new folder 
            name has an improper format.  The user is asked
            to enter a new directory name.
        FileExistsError: Raised if the folder to be created already exists.
            The program continues execution in this case.

    Returns:
        The same dictionary file as in the argument, but with the key
        'path' replaced with the output directory path.
    '''

    if output.getboolean('folder_prompt'):
        dir_lst = []

        if file.get('base'):
            for name in file['base']:  
                extra = 'for {0} '.format(name)

                while True:
                    print('What should the output directory ' + extra + 
                          'be known as?')
                    test_dir = input('>> ')
                    cls()

                    test_dir = directory_settings(dir_lst,test_dir,extra)

                    if test_dir:
                        dir_lst.append(test_dir)
                        break
        else:
            extra = ''

            while True:
                print('What should the output directory be known as?')
                test_dir = input('>> ')
                cls()

                test_dir = directory_settings(dir_list,test_dir)

                if test_dir:
                    dir_lst.append(test_dir)
                    break
    else:
        dir_lst = file['name']
        cls()

    # Create the dir_lst folders, continuing if the directory already exists.
    print('Saving output directories...')
    file['output'] = [os.path.join(file['directory'],name)
                      for name in dir_lst]

    for path in file['output']:
        try:
            os.makedirs(path)            
        except FileExistsError:
            continue
    cls()
    return file['output']

        
def directory_settings(dir_lst,test_dir,extra=''):
    
    test_dir = re.sub("[^\w-]*",'',test_dir)[0:50]

    if test_dir in dir_lst:
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

