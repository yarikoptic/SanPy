"""
nov sfn 2023, need to add aicsimageio for czi reading

pip install aicsimageio
pip install aicspylibczi

does not work on macos m1
conda install does not work!!!
"""

import os
from datetime import datetime

from setuptools import setup, find_packages

# manually keep in sync with sanpy/version.py
#VERSION = "0.1.11"

# with open(os.path.join('sanpy', 'VERSION')) as version_file:
#     VERSION = version_file.read().strip()

# load the readme
_thisPath = os.path.abspath(os.path.dirname(__file__))
with open(os.path.abspath(_thisPath+"/README.md")) as f:
    long_description = f.read()

# update _buildDateTime.py
_buildDate = datetime.today().strftime('%Y-%m-%d')
_buildTime = datetime.today().strftime('%H:%M:%S')
with open('sanpy/_buildDateTime.py', 'w') as f:
    f.write('# Auto generated in setup.py\n')
    f.write(f'BUILD_DATE="{_buildDate}"\n')
    f.write(f'BUILD_TIME="{_buildTime}"\n')

guiRequirements = [
    'numpy',  # ==1.23.4',  # 1.24 breaks PyQtGraph with numpy.float error
    'pandas',  #==1.5',  # version 2.0 removes dataframe append
    'scipy',
    'pyabf',
    'tifffile',
    
    # on 20231122 with newer 3.8.2 pyInstaller macOS app was hanging with 'building font cache'
    #'matplotlib==3.8.0',
    'matplotlib',
    
    'mplcursors',
    'seaborn',
    'requests', #  to load from the cloud (for now github)
    'tables',  # aka pytable for hdf5. Conflicts with conda install
    # used for line profile in kym analysis
    # 0.20.0 introduces pyinstaller bug because of lazy import
    # scikit-image 0.20.0 requires pyInstaller-hooks-contrib >= 2023.2.
    # and 0.22.0 requires >= 2023.10
    'scikit-image',  #==0.19.3', 
    'h5py',  # conflicts with conda install

    'qtpy',
    'pyqtgraph',
    'pyqtdarktheme',  # switched to this mar 2023
    'PyQt5',  # only install x86 version, need to use conda install pyqt
]

devRequirements = guiRequirements + [
    'mkdocs',
    'mkdocs-material',
    'mkdocs-jupyter',
    'mkdocstrings',
    'mkdocstrings-python', # resolve error as of April 30, 2023
    #'mkdocs-with-pdf',
    'tornado', # needed for pyinstaller
    'pyinstaller',
    'ipython',
    'jupyter',
    'tox',
    'pytest',
    'pytest-cov',
    'pytest-qt',
    'flake8',
]

testRequirements = guiRequirements + [
    'tox',
    'pytest',
    'pytest-cov',
    'pytest-qt',
    'flake8',
]

setup(
    name='sanpy-ephys',  # the package name (on PyPi), still use 'import sanpy'
    #version=VERSION,
    description='Whole cell current-clamp analysis.',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    url='http://github.com/cudmore/SanPy',
    author='Robert H Cudmore',
    author_email='rhcudmore@ucdavis.edu',
    license='GNU General Public License, Version 3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    # this is CRITICAL to import submodule like sanpy.userAnalysis
    packages=find_packages(include=['sanpy',
                                    'sanpy.*',
                                    'sanpy.interface',
                                    'sanpy.fileloaders'
                                    ]),
    
    include_package_data=True,  # uses manifest.in

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    # for conda based pyinstaller, we had to remove all installs
    # please install with pip install -e '.[gui]'
    install_requires=[],

    extras_require={
        'gui': guiRequirements,
        'dev': devRequirements,
        'test': testRequirements,
    },

    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'sanpy=sanpy.interface.sanpy_app:main',
        ]
    },
)
