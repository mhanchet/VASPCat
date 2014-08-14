import configparser
import os
import shutil

import pkg_resources as pkg

from vaspcat import cls,ExitError
from vaspcat.extend import configuration


def main(directory,overwrite=0) -> 'ConfigParser object':
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
    
    config = configparser.ConfigParser()
    user_config = configparser.ConfigParser()
    
    default_path = pkg.resource_filename('vaspcat','default.ini')
    with open(default_path, 'r') as default:
        config.read_file(default)
    user_path = os.path.join(directory,'config.ini')
    backup_path = pkg.resource_filename('vaspcat','backup.ini')
    
    cls()

    if overwrite == 0:
        print('Loading VaspCat settings...')
        
        if user_config.read(user_path):
            config = verify(config,user_config)
            print('User settings loaded from ' + 
                  '' + os.path.basename(directory) + '.\n')
            return config
        else:
            print('No user settings found in ' +
                  '' + os.path.basename(directory) + '.')
        
        print('VaspCat default settings loaded.\n')
        return config

    elif overwrite == 1:
        print('Changing VaspCat defaults...')    
        
        if user_config.read(user_path):
            config = verify(config,user_config)

            with open(default_path,'w') as default:
                config.write(default)
                print('VaspCat defaults overwritten.\n')
        else:
            print('No user settings found in ' + 
                  '' +os.path.basename(directory) + ' ' +
                  'to overwrite defaults with.\n')
    
    elif overwrite == 2:
        print('Reverting to original settings...')
        shutil.copyfile(backup_path,default_path)
        print('VaspCat settings restored.\n')

        
def verify(config,user_config):
    
    master = configuration.master

    for section in user_config.sections():
        for option in user_config.options(section):
            if section in master:
                if option in master[section].keys():
                    
                    value = user_config.get(section,option)
                    var_type = master[section][option][0]

                    if var_type == 'bool':
                        bool_lst = ['true','false']
                        if value.lower() not in bool_lst:
                            raise ExitError("User Settings Error",
                                    "Expected a boolean value for" +
                                    " " + option + " in section " + section +
                                    ",","but got " + value + ".",
                                    "Fix config.ini before loading " +
                                    "user settings.\n")

                    elif var_type == 'str':
                        str_lst = master[section][option][1]
                        value = value.lower().split()
                        
                        if not set(value).issubset(str_lst):
                            raise ExitError("User Settings Error",
                                    "Provided string value for" +
                                    " " + option + " in section" +
                                    " " + section + " is invalid.",
                                    "Fix config.ini before loading " +
                                    "user settings.\n",
                                    "Supplied values: " + ', '.join(value),
                                    "Supported values: " + 
                                    ", ".join(str_lst) + "\n")
                    
                    elif var_type == 'int':
                        try:
                            value = int(value)
                        except ValueError:
                            raise ExitError("User Settings Error",
                                    "Expected an integer value for" + 
                                    " " + option + " in section " + section +
                                    ",","but got " + value + ".",
                                    "Fix config.ini before loading " +
                                    "user settings.\n")

                        int_lst = master[section][option][1]
                        if value not in int_lst:
                            raise ExitError("User Settings Error",
                                    "Provided integer value for" +
                                    " " + option + " in section" +
                                    " " + section + " is invalid.",
                                    "Fix config.ini before loading " +
                                    "user settings.\n",
                                    "Supplied value: " + str(value),
                                    "Supported values: " + 
                                    ", ".join(map(str,int_lst)) + "\n")
                        
                    elif var_type == 'float':
                        try:
                            value = float(value)
                        except ValueError:
                            raise ExitError("User Settings Error",
                                    "Expected a decimal number for" + 
                                    " " + option + " in section " + section +
                                    ",","but got " + str(value) + ".",
                                    "Fix config.ini before loading " +
                                    "user settings.\n")
                    
                    elif var_type == 'path':
                        value = os.path.expandvars(value)
                        if not os.path.isdir(value):
                            raise ExitError("User Settings Error",
                                    "Expected a path name for" +
                                    " " + option + " in section " + section +
                                    ",", "but got " + value + ".",
                                    "Fix config.ini before loading " +
                                    "user settings.\n")
                else:
                    user_config.remove_option(section,option)
                    continue
            else:
                user_config.remove_section(section)
                break

    config.read_dict(user_config)
    return config

