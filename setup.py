from setuptools import setup, find_packages


setup(
    name = 'vaspcat',
    version = '0.1a1',
	author = 'Michael Carlson',
    
    #Default root is same directory as setup.py
    packages = find_packages(exclude=['*.test']),
    include_package_data = True,
	
	entry_points = {
        'console_scripts': [
            'vaspcat = vaspcat.application:main'
        ]
    }
)

    
