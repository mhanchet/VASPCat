import inspect
import os
import sys
from vaspcat.extend import posext


def main(directory) -> 'Atom list with same order as POSCAR':
    '''Calls methods which generate a POSCAR file for VASP usage.'''
    
    # Get list of file types that can be parsed.  This is accomplished
    # by grabbing class names in posext.py named after file extensions
    supported = [name.lower() for name, obj in inspect.getmembers(posext)
                 if inspect.isclass(obj)]
    
    print('Scanning for convertable files in {0}.'.format(directory),'\n')
    poscar = Convert(*find(directory, supported))

    print('Saving POSCAR file...')
    atom_list = poscar.output(directory)

    print('COMPLETE!','\n')
    return atom_list


def find(directory, supported) -> 'File path/extension tuple': 
    '''Finds files with supported extensions from directory.
    
    Args: 
        directory: Folder which vaspcat is run from, containing the 
                   files to be converted by the program.
        supported: List of file types which can be converted by
                   the program, obtained from class names in posext.py 
    '''

    # The use of slices is meant to remove the dot from the file extension.

    path = [os.path.join(directory, file)
            for ext in supported
            for file in os.listdir(directory)
            if file[-len(ext):] in supported]

    # Try to get the extension from the supported files, if files were found

    try: 
        file_ext = os.path.splitext(path[0])[1]

    except IndexError: 

        print('No convertable files were found in {0}.'.format(directory))
        print('Choose another directory and rerun vaspcat.','\n')
        print('Supported file formats: ' + ', '.join(Convert.supported))
        sys.exit()      

    return path[0], file_ext[-len(file_ext)+1:]

    
class Convert(object):
    '''Converts input files to POSCAR file'''

    def __init__(self, path, ext):
        '''Initialize the methods and functions output requires.

        Args:
            path: Location of file that will be converted.
            ext: The extension of the file which will be converted.
                 It is used to define read and parse methods for
                 the Convert class.  These methods are located in the
                 external file posext.py.
        '''
        
        #Account for the fact that classes are capitalized in posext.py        
        ext = ext.capitalize()
        
        self.path = path
        self.read = getattr(posext,ext).read
        self.parse = getattr(posext,ext).parse
    
    def output(self, directory) -> 'Atom list with same order as POSCAR':
        '''Saves POSCAR file in directory

        Args:
            directory: Specifies where the POSCAR file should be saved.

        Returns:
            List of atoms having the same order as the output POSCAR file.
            This information is found from element 0 in atom_info, a list
            having the following form:

            [[atom 1 name, # of atom 1], [atom 2 name, # of atom 2], ...]
        '''
        
        lat_vec, atom_info, frac_pos = self.parse(self.read(self.path))
 
        with open(os.path.join(directory, 'POSCAR'), mode='w') as f:
            #Line 1: System Name
            f.write(' '.join([atom[0] for atom in atom_info]) + '\n')

            #Line 2: Scaling Constant
            f.write('1.00'.rjust(7) + '\n')

            #Line 3: Lattice Vectors
            for line in lat_vec:
                f.write(' ' + line + '\n')

            #Line 4: Atoms per Species
            atom_count = ' '.join([str(count[1]) for count in atom_info])
            f.write(''.rjust(3) + atom_count + '\n')

            #Lines 5/6: Allow cell relaxation and specify direct coordinates
            f.write('Selective Dynamics\nDirect\n')

            #Lines 7-End: Cell Coordinates
            for line in frac_pos:
                f.write(' ' + line + '\n')

        return [atom[0] for atom in atom_info]  












        





         

    
    
                



    








    
