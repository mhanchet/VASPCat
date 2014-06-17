import os
import pkg_resources as pkg
import shutil
import sys

def main(directory, atom_list):
    print('Scanning for atom POTCAR files to combine','\n') 
    pkgfile = []
    for atom in atom_list:

        infile = pkg.resource_filename(
		    'vaspcat', 'extend/potext/POTCAR_' + atom
        )
        pkgfile.append(infile)
    
    print('Saving POTCAR file...')
    with open(os.path.join(directory,'POTCAR'),'w') as outfile:
        
        try:

            for file in pkgfile:
                with open(file, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)
	
        except IOError:

            errfile = os.path.basename(file)
            print("{0} was not found in the 'potext' directory.".format(errfile))
            print("Add {0} to the 'potext' folder, and run vaspcat again.".format(errfile))
            sys.exit()

    print('COMPLETE!','\n')
