import configparser
import os

from vaspcat import cls,ExitError


def main(config,file,suffix,i):
    '''Outputs KPOINTS file using data from config settings.'''

    kpoints = config['KPOINTS']

    with open(os.path.join(file['output'][i],'KPOINTS'+suffix), mode='w') as f:
        
        # Section 1: Comment line
        title_mode = int(kpoints['title_mode'])
        f.write(get_title(file,i,title_mode) + '\n')

        # Section 2: Number of KPOINTS
        f.write(kpoints['point_mode'] + '\n')

        # Section 3: Mesh specification line
        mode = int(kpoints['point_mode'])
        
        # Section 4: Coordinate data
        if mode == 0:
            f.write('Monkhorst-Pack\n')
            for var in ('x','y','z'):
                f.write(kpoints['mesh_' + var] + ' ')
            f.write('\n0 0 0')
        
        elif mode == 1:
            f.write('Reciprocal\n')
            f.write('0 0 0 1\n')


def get_title(file,i,title_mode):

    if title_mode == 0:
        return file['name'][i]

    elif title_mode == 1:
        while True:
            print('What should the KPOINT title of ' + file['name'][i] + ' be?')
            title = input('>> ')[0:50]
            cls()

            if not title:
                print("KPOINT title for " + file['name'][i] + " " +
                      "cannot be blank.")
                print("Enter a new title, or type 'exit' " +
                      "to return to the menu.\n")
            elif title.lower() == 'exit':
                raise ExitError('KPOINT Error',
                        'User stopped VaspCat while providing ' +
                        'KPOINT titles.\n')
            else:
                return title
    
    elif title_mode == 2:
        return 'KPOINTS'

