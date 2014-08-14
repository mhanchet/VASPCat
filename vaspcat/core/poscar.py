import decimal
import os
from vaspcat import cls,ExitError

def main(master,config,file,suffix,i):
    '''Outputs POSCAR file using data from master dictionary.'''
    
    poscar = config['POSCAR']
    with open(os.path.join(file['output'][i],'POSCAR'+suffix), mode='w') as f:
        
        # Title
        title_mode = int(poscar['title_mode'])
        f.write(get_title(file,i,title_mode) + '\n')
        
        # Scaling constant
        f.write(' 1.00\n')

        # Lattice vectors
        lat_vec = [['{: 15.10f}'.format(position) for position in vector]
                   for vector in master['lat_vec']]
        lat_vec = [' '.join(vector) for vector in lat_vec]

        for vector in lat_vec:
            f.write(' ' + vector + '\n')

        # Atom symbol (optional)
        if poscar.getboolean('atom_label'):
            f.write(' ') 
            for name in sorted(set(master['atom'])):
                f.write('{:6} '.format(name))
            f.write('\n')

        # Atom count
        atom_set = sorted(set(master['atom']))
        f.write(' ')
        
        for name in atom_set:
            f.write('{:<6} '.format(master['atom'].count(name)))
        f.write('\n')
        
        # Cell relaxation (optional)
        if poscar.getboolean('selective_dynamics'):
            f.write('Selective Dynamics\n')
            flag = 'F F F'
        else:
            flag = ''

        # Specify coordinates are fractional
        f.write('Direct\n')

        # Write fractional coordinates
        for atom in atom_set:
            for i,name in enumerate(master['atom']):
                if atom == name:
                    f.write('   {:12.10f} {:12.10f} {:12.10f} '.format(
                        master['x'][i],master['y'][i],master['z'][i]) + flag +
                        '\n')


def get_title(file,i,title_mode):
    
    if title_mode == 0:
        return file['name'][i]
    
    elif title_mode == 1:
        return file['base'][i]
    
    elif title_mode == 2:
        while True:
            print('What should the POSCAR title of ' + file['base'][i] + ' be?')
            title = input('>> ')[0:50]
            cls()

            if not title:
                print("POSCAR title for " + file['base'][i] + " " +
                      "cannot be blank.")
                print("Enter a new title, or type 'exit' " +
                      "to return to the menu.\n")
            elif title.lower() == 'exit':
                raise ExitError('POSCAR Error',
                        'User stopped VaspCat while providing ' +
                        'POSCAR titles.\n')
            else:
                return title
        
    elif title_mode == 3:
        return 'POSCAR'
    
