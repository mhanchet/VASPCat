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
    Sets up top level VaspCat package and defines custom error handling class.
"""


import os

__version__ = '0.1a3'

# When called, clear the current text from the terminal screen.
cls = lambda: os.system('clear') or None 


class ExitError(Exception):
    """Custom error class for abandoning VaspCat output.
    
    Attributes:
        title: Name of the error shown to the user.  A colon and newline
            character are appended to the title string.
        *args: String list containing the description of the error shown to 
            the user.  Each argument is printed on a separate line.
    """
    
    def __init__(self,title,*args):
        
        self.title = title+':\n'
        self.args = args

    def __str__(self):

        err_msg = self.title + '\n'.join(self.args)
        return err_msg

