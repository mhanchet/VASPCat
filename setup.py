from setuptools import setup, find_packages


setup(
    name = 'VaspCat',
    version = '0.1a2',
    url = 'https://github.com/mcarl15/VaspCat',
    license = 'GNU v3',
    author = 'Michael Carlson',
    author_email = 'mcarl15@ksu.edu'
    description = 'User-friendly VASP DFT input file generator',

    #Default root is same directory as setup.py
    packages = find_packages(exclude=['*.test']),
    include_package_data = True,
	
	entry_points = {
        'console_scripts': [
            'vaspcat = vaspcat.application:main'
        ]
    }
)

    
