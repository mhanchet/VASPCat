import os

from vaspcat import ExitError


def main(master,config,file,suffix,i):
    
    potcar = config['POTCAR']
    atom_set = sorted(set(master['atom']))
    directory = os.path.expandvars(potcar['path'])
    path = []

    for atom in atom_set:
        in_file = os.path.join(directory,atom,'POTCAR')
        path.append(in_file)
     
    atom_lst = []
    for in_file,atom in zip(path,atom_set):
        if not os.path.isfile(in_file):
            atom_lst.append(atom)
    
    if len(atom_lst) > 0:
        atom_str = ', '.join(atom_lst)
        raise ExitError('POTCAR Error', 'Required POTCAR files were not ' +
                        'found in ' + os.path.basename(directory) + '.',
                        'Add the missing files, and run VaspCat again.\n',
                        'Missing atoms: {0}\n'.format(atom_str))
    else:
        out_file = os.path.join(file['output'][i],'POTCAR'+suffix)
        with open(out_file,'a') as fout:
            for in_file,atom in zip(path,atom_set):
                with open(in_file,'r') as fin:
                    for line in fin:
                        fout.write(line)   
        
