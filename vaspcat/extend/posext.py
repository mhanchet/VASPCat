import re
import shlex
from math import sin,cos,radians


def cif_read(file) -> 'Dictionary for cif_Parse()':
    '''Gathers variable info from input cif file.

    Args:
        file: Full path of the .cif file to be read.

    Returns:
        A dictionary object containing cif file variables as keys and their
        values, which are stored as lists of strings.
    '''

    # Store each line from input file in a list.  Each list element is divided
    # into its individual parts by the method shlex.split.  Shlex is part of
    # the standard library, and the split method separates words with spaces 
    # between them and phrases contained in quotes.  For example, suppose the
    # following line was read from a cif file:
    #
    #     _audit_creation_method   'Materials Studio'
    #
    # Shlex.split would create the following list from the line:
    #
    #    ['_audit_creation_method', 'Material Studio']
    #
    # The argument 'posix = False' ensures that ungrouped quotation marks and
    # apostrophes within a string are ignored.
    
    with open(file, 'r+') as f:
        lines_read = [shlex.split(line.strip(), posix = False)
                      for line in f
                      if line[:-2] != ''            
                      if not line.startswith(('#',';', 'data_'))]

    # Generate a dictionary called output that links .cif variable names to
    # the data they contain.  If the phrase loop_ is found in a cif file, 
    # multiple variables can be initialized at once. These multiple variables
    # are given values on a separate line, with each value separated by
    # spaces.  The following cif file code illustrates this:
    #
    #   1  loop_
    #   2  _geom_bond_atom_site_label
    #   3  _geom_bond_distance
    #   4  O18  1.229
    #
    # In this code, the variables '_geom_bond_atom_site_label' and
    # '_geom_bond distance' are set equal to O18 and 1.229 respectively in
    # line 4.
    #
    # The attribute 'keyword' accounts for the possibility of
    # cif loops by storing loop variable in a list before assignment
    # occurs.  If there are more keywords then values to be assigned
    # in a loop, the values that are present are stored in 'line_list'.
    # If we have more values than variables, the values present are combined
    # into a single string and stored in 'line_list' as well.
    #
    # The contents of line_list are mapped to the keywords in different ways
    # in the if statements below.  See code for details.
    
    output, keyword, line_list = {}, [], []

    for line in lines_read:

        if line[0].startswith('loop'):
            keyword = line_list = []

        elif line[0].startswith('_'):                 
            if len(line) == 2:  #if variable and value are adjacent
                keyword = line_list = []
                output[line[0]] = line[1]
            else:  #if variable is in a loop
                keyword.append(line[0])
                line_list = []
                output[keyword[-1]] = []
                
        elif len(keyword) != len(line + line_list):
            if len(keyword) < len(line + line_list): #if too few keywords
                line_list.append(' '.join(line))
                output[keyword[-1]].extend(line_list)
                line_list = []
            elif len(keyword) > len(line + line_list): #if too few variables
                line_list.append(line)

        elif len(keyword) == len(line + line_list): #if variables equal values
            line_list.extend(line)
            for (key, value) in zip(keyword, line_list): 
                output[key].append(value)
            line_list = []

    return output


def cif_parse(data) -> '3-tuple for Convert.output()':
    '''Takes data from cif_Read function and returns relevant data

    Args:
        data: Dictionary from cif_read mapping cif variables to values.

    Returns:
        A 3-tuple containng the required information for Convert.output().

        lat_vec: A list of three strings containing the lattice vectors
        atom_info: A list with the following form -
            [[atom 1 name, # of atom 1], [atom 2 name, # of atom 2], ...]
        frac_coor: A list of strings, with each string containing the
                   x, y, and z fractional coordinates of the atom
                   separated by spaces.
    '''
    
    # Remap keywords in data to new keys.  Choose of the two possible
    # atom labels in the process (either '_atom_site_type symbol'
    # or '_atom_site_label'
    
    keyword = ['_cell_' + label
               for label in ('length_a','length_b','length_c',
                             'angle_alpha', 'angle_beta', 'angle_gamma')]

    keyword += ['_atom_site_' + label
                for label in ('fract_x','fract_y','fract_z',
                              'type_symbol','label')]

    newKey = ['x', 'y', 'z' , 'atom',
              'alpha', 'beta', 'gamma', 'a', 'b', 'c']

    if data.get('_atom_site_type_symbol'):
        if data.get('_atom_site_label'):
            keyword.remove('_atom_site_label')
 
    keys = sorted([key for key in keyword if data.get(key)])
    keys = zip(keys, newKey)

    f = {k[1] : data[k[0]] for k in keys}
    
    # Convert all numbers to floats, with sub removing unneeded characters
    # Since the largest possible element name is two letters, re.sub is 
    # used to remove extraneous numbers and capital letters from the second
    # character of the 'atom' variable.  Sometimes, cif authors include
    # sig fig info in parentheses, so we need to strip out these
    # brackets with re.sub before calculations can be made.
    
    for key, value in f.items():
       
        if key == 'atom':
            atom = [f[0] + re.sub('[^a-z]','',f[1:2]) for f in value]

        elif key in ['alpha', 'beta', 'gamma']:
            f[key] = radians(float(re.sub('[()]','',value)))

        elif key in ['a', 'b', 'c']:
            f[key] = float(re.sub('[()]','',value)) 

        elif key in ['x', 'y', 'z']:
            f[key] = [float(re.sub('[()]','',item)) for item in value]
    
    # Calculate the lattice vectors, outputting as string list.
    # v is the unit cell volume.

    v = (f['a']*f['b']*f['c']*
         (1 - cos(f['alpha'])**2 - cos(f['beta'])**2 - cos(f['gamma'])**2 +
          2*cos(f['alpha'])*cos(f['beta'])*cos(f['gamma']))**0.5)

    lat_vec = [[f['a'], f['b']*cos(f['beta']), f['c']*cos(f['beta'])],
               [0, f['b']*sin(f['gamma']),
                f['c']*(cos(f['alpha'])- cos(f['beta'])*cos(f['gamma']))/
                sin(f['gamma'])],
               [0, 0, v/(f['a']*f['b']*sin(f['gamma']))]]

    lat_vec = [' '.join(['{: 5.10f}'.format(i) for i in v]) for v in lat_vec]

    #Combine x, y, and z fractional coordinates in a string.
    
    frac_coor = [' '.join(['{: 5.10f}'.format(i) for i in tup]) 
                 for tup in zip(f['x'], f['y'], f['z'])]

    # Create the remaining two output lists from the set uniq_atom.
    # The order of the fractional coordinates now matches the atom
    # order in atom_info.

    uniq_atom = set(atom)

    atom_info = [(a, atom.count(a)) for a in uniq_atom]
    frac_coor = [f for ua in uniq_atom for a, f in zip(atom, frac_coor)
                 if ua == a]

    return lat_vec, atom_info, frac_coor


def pdb_read(file) -> 'Dictionary for pdb_Parse()':
    '''Gathers variable info from input pdb file.

    Args:
        file: Full path of the .pdb file to be read.

    Returns:
        A dictionary object containing pdb file variables as keys and their
        values, which are stored as lists of either strings or floats.
    '''

    keyword = ('CRYST1', 'SCALE', 'ATOM', 'HETATM')

    with open(file, 'r+') as f:
        lines_read = [line for line in f if line.startswith(keyword)]

    output = {'x':[], 'y':[], 'z':[], 'atom':[]}

    # Set value of keys in output based on field position on a given line.
    # In a pdb file, every line starts with a record name in all caps.
    # Next to each record are fields representing different variable values.
    # The fields are always located in the same position next to a record.
    # The if statements take advantage of this consistency, reading fields
    # from the same position in a line if a record name is recognized.
    
    for line in lines_read:

        if line.startswith('CRYST1'):
            output['a'] = float(line[6:15].strip())
            output['b'] = float(line[15:24].strip())
            output['c'] = float(line[24:33].strip())

            output['alpha'] = radians(float(line[33:40])) 
            output['beta'] = radians(float(line[40:47]))
            output['gamma'] = radians(float(line[47:54]))

        elif line.startswith('SCALE'):
            output['s' + line[5]] = [float(line[10:20].strip()),
                                     float(line[20:30].strip()),
                                     float(line[30:40].strip())]

            output['u' + line[5]] = float(line[45:55].strip())
            
        elif line.startswith(('ATOM', 'HETATOM')):
            if line[12].upper() == 'H':
                output['atom'].append(line[12])
            elif line[12] == ' ':
                output['atom'].append(line[13])
            else:
                output['atom'].append(line[12] + line[13].lower())
            
            output['x'].append(float(line[30:38].strip()))
            output['y'].append(float(line[38:46].strip()))
            output['z'].append(float(line[46:54].strip()))

    return output
            
                                        
def pdb_parse(data) -> '3-Tuple for Convert.Output()':
    '''Takes data from cif_Read function and returns relevant data

    Args:
        data: Dictionary from cif_read mapping cif variables to values.

    Returns:
        A 3-tuple containing the required information for Convert.output().

        lat_vec: A list of three strings containing the lattice vectors
        atom_info: A list with the following form -
            [[atom 1 name, # of atom 1], [atom 2 name, # of atom 2], ...]
        frac_coor: A list of strings, with each string containing the
                   x, y, and z fractional coordinates of the atom
                   separated by spaces.
    '''
    f = data
    
    #Convert the supplied orthogonal coordinates to fractional coordinates.

    xyz = list(zip(f['x'], f['y'], f['z']))
    ortho = [vec for vec in xyz]

    key_tup = (('x','1'),('y','2'), ('z','3'))

    for key,i in key_tup:
        s = 's' + i
        u = 'u' + i
        f[key] = [f[s][0]*vec[0] + f[s][1]*vec[1] + f[s][2]*vec[2] + f[u]
                     for vec in ortho]
    
    # Calculate the lattice vectors, outputting as string list.
    # v is the unit cell volume.

    v = (f['a']*f['b']*f['c']*
        (1 - cos(f['alpha'])**2 - cos(f['beta'])**2 - cos(f['gamma'])**2 +
         2*cos(f['alpha'])*cos(f['beta'])*cos(f['gamma']))**0.5)

    lat_vec = [[f['a'], f['b']*cos(f['beta']), f['c']*cos(f['beta'])],
               [0, f['b']*sin(f['gamma']),
                f['c']*(cos(f['alpha'])- cos(f['beta'])*cos(f['gamma']))/
                sin(f['gamma'])],
               [0, 0, v/(f['a']*f['b']*sin(f['gamma']))]]

    lat_vec = [' '.join(['{: 5.10f}'.format(i) for i in v]) for v in lat_vec]

    #Combine x, y, and z fractional coordinates in a string.
    
    frac_coor = [' '.join(['{: 5.10f}'.format(i) for i in tup]) 
                 for tup in zip(f['x'], f['y'], f['z'])]

    # Create the remaining two output lists from the set uniq_atom.
    # The order of the fractional coordinates now matches the atom
    # order in atom_info.

    atom = f['atom']
    uniq_atom = set(atom)

    atom_info = [(a, atom.count(a)) for a in uniq_atom]
    frac_coor = [f for ua in uniq_atom for a, f in zip(atom, frac_coor)
                 if ua == a]

    return lat_vec, atom_info, frac_coor
                

    
    

            
            









    
