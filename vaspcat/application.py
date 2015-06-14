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
    Contains VaspCat program menu UI and calls to file processing methods.   
"""


import configparser
import os

from vaspcat import cls,ExitError,__version__           # Globals
from vaspcat import ExitError,output,reader,settings    # Classes/Modules


def main():
    """Entry point into the VaspCat program.
    
    Returns:
        String with exit message upon program termination.
    """
    
    cls()
    file = {'directory':os.getcwd()}

    tab = ''.ljust(2)
    title_text = ('[VaspCat DFT Toolkit] v' + __version__ + '\n' +
                  'Type the number of the option you wish to select.\n')
    menu_text = ('MAIN MENU\n'+
                 tab+'(0) Start file output\n'+
                 tab+'(1) Edit default settings\n'+
                 tab+'(2) Print config file\n' +
                 tab+'(3) Exit program\n')

    # Main program loop
    while True:
        print(title_text)
        print(menu_text)
        choice = input('>> ')
    
        if choice == '0': 
            cls() 
            
            try:
                config = settings.main(file['directory'])
                file = reader.main(config,file)
                output.main(config,file)
                print('Complete!','\n')
            
            except ExitError as exit:
                cls()
                print(exit)
        
        elif choice == '1': 
            cls()
            
            while True:
                print('EDIT DEFAULTS\n' +
                      tab+'(0) Write user config to default\n' +
                      tab+'(1) Restore program defaults\n' +
                      tab+'(2) Return to menu\n')
                choice = input('>> ')
            
                try:
                    if choice == '0':
                        settings.main(file['directory'],overwrite=1)
                        break
                    elif choice == '1':
                        settings.main(file['directory'],overwrite=2)
                        break
                    elif choice == '2':
                        cls()
                        break
                    else:
                        cls()
                        print("Invalid selection '" + choice + "'.") 
                        print("Enter a valid numeric choice.\n")
                except ExitError as exit:
                    cls()
                    print(exit)

        elif choice == '3': 
            cls()
            return 'Exiting VaspCat... '  
        
        else:
            cls()
            print("Invalid selection '" + choice + "'.")
            print("Enter a valid numeric choice.\n")

