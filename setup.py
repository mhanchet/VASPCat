from setuptools import setup, find_packages


setup(
    name = 'VaspCat',
    version = '0.1a2',
	author = 'Michael Carlson',
    url = 'https://github.com/mcarl15/VaspCat',
    license = 'GNU v3',

    #Default root is same directory as setup.py
    packages = find_packages(exclude=['*.test']),
    include_package_data = True,
	
	entry_points = {
        'console_scripts': [
            'vaspcat = vaspcat.application:main'
        ]
    }
)

    
