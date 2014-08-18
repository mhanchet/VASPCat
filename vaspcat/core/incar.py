import configparser
import os

from vaspcat import cls,ExitError


def main(config,file,suffix,i):
    '''Outputs INCAR file using data from config settings.'''

    incar = config['INCAR']
    
    with open(os.path.join(file['output'][i],'INCAR'+suffix), mode='w') as f:
        
        # Section 1: System name
        if incar['system'].lower() != 'none':
            title_mode = int(incar['system'])
            f.write('SYSTEM = ' + get_title(file,i,title_mode)+'\n\n')

        # Section 2: Parallel computing options
        if incar['npar'].lower() != 'none':
            f.write('Parallelisation options:\n')
            f.write('  NPAR = ' + incar['npar']+'\n\n')

        # Section 3-4: Remaining options
        section = {'File output options:\n':['LWAVE','LCHARG'],
                   'Calculation options:\n':['ENCUT','EDIFF','EDIFFG',
                                               'ISMEAR','GGA','ISPIN']}
        for header in section:
            flag = 0
            
            for name in section[header]:
                if incar[name.lower()] != 'none' and flag == 0:
                    flag = 1
                    f.write(header)
                if incar[name.lower()] != 'none':
                    f.write('  ' + name + ' = ' + get_capital(incar,name) + 
                            '\n')
            if flag == 1:
                f.write('\n')
   

def get_title(file,i,title_mode):

    if title_mode == 0:
        return file['name'][i]

    elif title_mode == 1:
        while True:
            print('What should the INCAR title of ' + file['name'][i] + ' be?')
            title = input('>> ')[0:50]
            cls()

            if not title:
                print("INCAR title for " + file['name'][i] + " " +
                      "cannot be blank.")
                print("Enter a new title, or type 'exit' " +
                      "to return to the menu.\n")
            elif title.lower() == 'exit':
                raise ExitError('INCAR Error',
                        'User stopped VaspCat while providing ' +
                        'INCAR titles.\n')
            else:
                return title
    
    elif title_mode == 2:
        return 'INCAR'


def get_capital(incar,name):
    
    value = incar[name.lower()].lower()

    if value in ['true','false']:
        if value == 'true':
            return '.TRUE.'
        elif value == 'false':
            return '.FALSE.'
    else:
        return value.upper()

