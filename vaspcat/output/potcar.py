import os
import pkg_resources as pkg
import shutil
import sys

def main(directory, atom_list):
    '''Combines POTCAR files from potext in POSCAR order

    Args:
        directory: Directory vaspcat is run from, used for POSCAR output path.
        atom_list: List of atom names with same order as in POSCAR file.
                   Used to get atomic POSCAR files stored in /potext/atom_name

    Exceptions:
        IOError: Occurs when POTCAR file for a particular atom is not found
                 in the potext directory.  

    Returns:
        String indicating that POTCAR generation has completed.

    '''
    
    # Use the pkg_resources module to get the path of the atomic POTCAR file
    # stored in potext/atom.  Add this path to the pkgfile list.

    print('Scanning for atom POTCAR files to combine','\n') 
    pkgfile = []
    for atom in atom_list:

        infile = pkg.resource_filename(
		    'vaspcat', 'extend/potcar/' + atom + '/POTCAR'
        )
        pkgfile.append(infile)
    
    # Create an output file named POSCAR.  Use the shutil module to bring
    # the contents of the pkgfile files into the output POTCAR.

    print('Saving POTCAR file...')
    with open(os.path.join(directory,'POTCAR'),'w') as outfile:
        
        try:

            for file in pkgfile:
                with open(file, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)
	
        except IOError:
            
            # Indicate to the user where the missing POTCAR file should go.
            
            errfile = os.path.basename(os.path.dirname(file))
            print("{0} was not found in the "
                  "'potext' directory.".format(errfile))
            print("Add {0}/POTCAR to the 'potext' folder, and "
                  "run vaspcat again.".format(errfile))
            sys.exit()

    return 'COMPLETE!\n'
