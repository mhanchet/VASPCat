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
    Provides VaspCat with required settings in the proper format.   
"""


import configparser
import os
import shutil

from vaspcat import cls,ExitError
from vaspcat.extend import configuration


def main(directory,overwrite=0):
    """Supplies 'config' with VaspCat settings read from file.
    
    Args:
        directory(str):  The folder the user started VaspCat in.
            This directory is searched for user config.ini files.
        overwrite(int): Optional parameter specifying if the file containing
            the default settings should be overwritten.
            
            0 (default) - Do not overwrite default.ini.  Read user settings
                into config, or default settings if user has not supplied any.
            1 - Overwrite default.ini with user supplied config.ini.
            2 - Restore default settings by overwriting default.ini with
                backup.ini. 

    Returns:
        config(ConfigParser): Contains the sections and options specifying
            VaspCat behavior.
    """
    
    config = configparser.ConfigParser()
    user_config = configparser.ConfigParser()
    
    vaspcat_path = os.path.dirname(os.path.abspath(__file__))
    user_path = os.path.join(directory,'config.ini')
    backup_path = os.path.join(vaspcat_path,'backup.ini')

    default_path = os.path.join(vaspcat_path,'default.ini')
    with open(default_path, 'r') as default:
        config.read_file(default)
        
    cls()

    if overwrite == 0:
        print('Loading VaspCat settings...')
        
        if user_config.read(user_path):
            config = verify(config,user_config)
            print('User settings loaded from ' + 
                  '' + os.path.basename(directory) + '.\n')
        else:
            print('No user settings found in ' +
                  '' + os.path.basename(directory) + '.\n' +
                  '' + 'VaspCat default settings loaded.')
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
                  '' + os.path.basename(directory) + ' ' +
                  'to overwrite defaults with.\n')
    
    elif overwrite == 2:
        print('Restoring original settings...')
        shutil.copyfile(backup_path,default_path)
        print('VaspCat settings restored.\n')

        
def verify(config,user_config):
    """Ensures the user has supplied settings in the correct format.
    
    Args:
        config(ConfigParser): Settings file that is overwritten by user_config
            after the user provided options are validated.
        user_config(ConfigParser): Settings provided by the user which are
            compared to the sections and options found in
            vaspcat/extend/configuration.py.

    Raises:
        ExitError: Occurs when user gives an unrecognized option to config.py.
        ValueError: Occurs when a string is entered as a value for an option
            which requires a number as input.

    Returns:
        config(ConfigParser): Updated settings with extraneous options and
            sections removed.
    """   
    
    # Master is a dictionary containing all of the possible VaspCat settings  
    master = configuration.items()
    
    for section in user_config.sections():
        for option in user_config.options(section):
            if section in master:
                if option in master[section].keys():
                    
                    value = user_config.get(section,option)
                    variable_type = master[section][option][0]
                    
                    if section == 'INCAR' and value.lower() == 'off':
                        continue

                    elif variable_type == 'bool':
                        boolean_list = ['true','false']
                        if value.lower() not in boolean_list:
                            raise ExitError('User Settings Error',
                                    'Expected a boolean value for' +
                                    ' ' + option + ' in section ' + section +
                                    ',','but got ' + value + '.',
                                    'Fix config.ini before loading ' +
                                    'user settings.\n')

                    elif variable_type == 'str':
                        string_list = master[section][option][1]
                        value = value.lower().split()
                        
                        if not set(value).issubset(string_list):
                            raise ExitError('User Settings Error',
                                    'Provided string value for' +
                                    ' ' + option + ' in section' +
                                    ' ' + section + ' is invalid.',
                                    'Fix config.ini before loading ' +
                                    'user settings.\n',
                                    'Supplied values: ' + ', '.join(value),
                                    'Supported values: ' + 
                                    ', '.join(string_list) + '\n')
                    
                    elif variable_type == 'int':
                        try:
                            value = int(value)
                        except ValueError:
                            raise ExitError('User Settings Error',
                                    'Expected an integer value for' + 
                                    ' ' + option + ' in section ' + section +
                                    ',','but got ' + value + '.',
                                    'Fix config.ini before loading ' +
                                    'user settings.\n')

                        low = master[section][option][1]
                        high = master[section][option][2]

                        if not low <= value <= high:
                            raise ExitError('User Settings Error',
                                    'Provided integer value for' +
                                    ' ' + option + ' in section' +
                                    ' ' + section + ' is invalid.',
                                    'Fix config.ini before loading ' +
                                    'user settings.\n',
                                    'Supplied value: ' + str(value),
                                    'Supported values: ' + 
                                    '{0} to {1}\n'.format(low,high))
                        
                    elif variable_type == 'float':
                        try:
                            value = float(value)
                        except ValueError:
                            raise ExitError('User Settings Error',
                                    'Expected a decimal number for' + 
                                    ' ' + option + ' in section ' + section +
                                    ',','but got ' + str(value) + '.',
                                    'Fix config.ini before loading ' +
                                    'user settings.\n')
                    
                    elif variable_type == 'path':
                        value = os.path.expandvars(value)
                        if not os.path.isdir(value):
                            raise ExitError('User Settings Error',
                                    'Expected a path name for' +
                                    ' ' + option + ' in section ' + section +
                                    ',', 'but got ' + value + '.',
                                    'Fix config.ini before loading ' +
                                    'user settings.\n')
                else:
                    user_config.remove_option(section,option)
                    continue
            else:
                user_config.remove_section(section)
                break

    config.read_dict(user_config)
    return config

