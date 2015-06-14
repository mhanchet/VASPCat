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
    Allows the user to add keys to the 'master' dictionary that will be 
    recognized by VaspCat when reading user defined settings. 
"""


import inspect

from vaspcat.extend import filetype


def items(setting=True):
    """Initializes config wtih settings required for VaspCat to run.
    
    Args:
        setting(bool) Optional variable which changes what object the method
            returns to its calling function.

    Returns:
        if setting:
            master(dict): Each key is a section name and each value is a 
                possible option within that section.  The options themselves 
                are dictionaries, with the key as the option name and their 
                values as a list based on the option variable type.  
                The contents of each list are as follows - 
                
                bool: Contains the word 'bool' at index 0.
                float: Contains the word 'float' at index 0.
                int: Contains the word 'int' at index 0, the lower bound on the
                    integer value at index 1, and the upper bound at index 2.
                path: Contains the word 'path' at index 0.
                str: Contains the word 'str' at index 0 and a list of possible
                    values for the option at index 1.
        else:
            supported(list): File types that can be parsed by VaspCat, based
                on the class names in /vaspcat/extend/filetype.
    """
    
    # Ignore the 'Counter' class name, which is used by filetype.py.
    supported = [name.lower()
                 for name,obj in inspect.getmembers(filetype)
                 if inspect.isclass(obj) if name != 'Counter'] + ['all','none']
    if setting:
        master = {'READER':{'file_type_read':['str',supported],
                            'name_prompt':['bool']},
                  'OUTPUT':{'folder_output':['bool'],
                            'folder_prompt':['bool'],
                            'name_as_suffix':['bool'],
                            'poscar':['bool'],
                            'potcar':['bool']},
                  'POSCAR':{'atom_label':['bool'],
                            'selective_dynamics':['bool'],
                            'title_mode':['int',0,4]},
                  'POTCAR':{'path':['path']},
                  'INCAR':{'algo':['str',['none','nothing','exact','diag',
                                          'a','c','d','e','f','n','s','v']],
                           'ediff':['float'],
                           'ediffg':['float'],
                           'encut':['float'],
                           'enmax':['float'],
                           'gga':['str',['91','pe','rp','ps','am']],
                           'ibrion':['str',['-1','0','1','2','3','5','6','7',
                                            '8','44']],
                           'icharg':['0','1','2','4'],
                           'idipol':['int',1,4],
                           'isif':['int',0,6],
                           'ismear':['int',-5,2],
                           'ispin':['int',1,2],
                           'istart':['int',0,2],
                           'lcharg':['bool'],
                           'lorbit':['str',['0','1','2','5','10','11','12']],
                           'lreal':['str',['a','auto','false','o',
                                           'on','true']],
                           'lwave':['bool'],
                           'nelm':['int',0,100],
                           'npar':['int',1,16],
                           'nsw':['int',0,1000],
                           'potim':['float'],
                           'sigma':['float'],
                           'system':['int',0,2]},
                  'KPOINTS':{'mesh_x':['int',1,50],
                             'mesh_y':['int',1,50],
                             'mesh_z':['int',1,50],
                             'point_mode':['int',0,1],
                             'title_mode':['int',0,2]}}
        return master
    else:
        return supported
     
