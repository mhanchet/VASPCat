import os
import shutil

from vaspcat import ExitError


def main(master,config,file,suffix,i):
    
    potcar = config['POTCAR']
    atom_set = sorted(set(master['atom']))
    directory = os.path.expandvars(potcar['path'])
    path = []
    
    for atom in atom_set:
        in_file = os.path.join(directory,atom,'POTCAR')
        path.append(in_file)
    
    data = zip(path,atom_set)
    atom_lst = []

    for in_file,atom in data:
        if not os.path.isfile(in_file):
            atom_lst.append(atom)
    
    if len(atom_lst) > 0:
        atom_str = ', '.join(atom_lst)
        raise ExitError('POTCAR Error', 'Required POTCAR files were not ' +
                        'found in ' + os.path.basename(directory) + '.',
                        'Add the missing files, and run VaspCat again.\n',
                        'Missing atoms: {0}\n'.format(atom_str))
    else:
        out_file = open(os.path.join(file['output'][i],'POTCAR'+suffix),'w')
        for in_file,atom in data:
            shutil.copyfileobj(in_file, out_file)        
        out_file.close()
