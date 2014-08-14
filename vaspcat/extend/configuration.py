import inspect

from vaspcat.extend import filetype

supported = [name.lower() 
             for name,obj in inspect.getmembers(filetype)
             if inspect.isclass(obj)] + ['all','none']

master = {'READER':{'file_type_read':['str',supported],
                    'name_prompt':['bool']},
          'OUTPUT':{'folder_output':['bool'],
                    'folder_prompt':['bool'],
                    'name_as_suffix':['bool'],
                    'poscar':['bool'],
                    'potcar':['bool']},
          'POSCAR':{'title_mode':['int',[0,1,2,3,4]],
                    'atom_label':['bool'],
                    'selective_dynamics':['bool']},
          'POTCAR':{'path':['path']}}


