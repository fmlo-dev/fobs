from setuptools import setup

setup(name = 'fobs',
      description = 'convert 45m/ASTE obstable to one for FMLO observation',
      version = '0.1',
      author = 'astropenguin',
      author_email = 'taniguchi@a.phys.nagoya-u.ac.jp',
      url = 'https://github.com/fmlo-dev/fobs',
      packages = ['fobs'],
      entry_points = {'console_scripts': ['fobs=fobs.cli:main']},
      install_requires = ['docopt', 'pyyaml'])
