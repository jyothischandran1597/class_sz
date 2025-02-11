from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as nm
import os
import subprocess as sbp
import os.path as osp

# this file is currently what works on M1.
# Recover the gcc compiler
GCCPATH_STRING = sbp.Popen(
    # ['gcc-11', '-print-libgcc-file-name'],
    ['gcc', '-print-libgcc-file-name'],
    stdout=sbp.PIPE).communicate()[0]
GCCPATH = osp.normpath(osp.dirname(GCCPATH_STRING)).decode()

liblist = ["class"]
MVEC_STRING = sbp.Popen(
    # ['gcc-11', '-lmvec'],
    ['gcc', '-lmvec'],
    stderr=sbp.PIPE).communicate()[1]
if b"mvec" not in MVEC_STRING:
    liblist += ["mvec","m"]

# define absolute paths
root_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
include_folder = os.path.join(root_folder, "include")
classy_folder = os.path.join(root_folder, "python")

# Recover the CLASS version
with open(os.path.join(include_folder, 'common.h'), 'r') as v_file:
    for line in v_file:
        if line.find("_VERSION_") != -1:
            # get rid of the " and the v
            VERSION = line.split()[-1][2:-1]
            break

# Define cython extension and fix Python version
classy_ext = Extension("classy_sz", [os.path.join(classy_folder, "classy.pyx")],
                           #include_dirs=[nm.get_include(), include_folder,'/Users/boris/gsl-2.6/include'],
                           include_dirs=[nm.get_include(), include_folder],
                           libraries=liblist,
                           library_dirs=[root_folder, GCCPATH],
                           #extra_link_args=['-lgomp','-Wl,-rpath,/usr/local/opt/gcc/lib/gcc/10/','-L/Users/boris/gsl-2.6/lib/','-lgsl','-lgslcblas'])
                           #extra_link_args=['-lgomp','-L/Users/boris/gsl-2.6/lib/','-lgsl','-lgslcblas','-Wl,-rpath,/usr/local/opt/gcc/lib/gcc/10/'])
                           # extra_link_args=['-lgomp','-lgsl','-lfftw3','-lgslcblas','-Wl,-rpath,/usr/local/opt/gcc/lib/gcc/11/']) # BB
                           # extra_link_args=['-lomp','-L/Users/boris/miniconda/lib','-lgsl','-lfftw3','-lgslcblas']) # BB
                           #extra_link_args=['-lomp','-L/Users/boris/opt/miniconda3/lib','-lgsl','-lfftw3','-lgslcblas']) # BB
                           extra_link_args=['-lomp','-L//home/jyothis/.pyenv/versions/class-sz/lib','-lgsl','-lfftw3','-lgslcblas']) # BB
                           # extra_link_args=['-lomp','-L/Users/boris/opt/anaconda3/lib','-lgsl','-lfftw3','-lgslcblas']) # BB

                           #extra_link_args=['-lgomp','-lgsl','-lfftw3_omp','-lfftw3','-lgslcblas','-Wl,-rpath,/usr/local/opt/gcc/lib/gcc/11/']) # BB
                           # extra_link_args=['-lgomp','-L/home/runner/work/SOLikeT/SOLikeT/gsl-2.6/lib','-lgsl','-lgslcblas'])

import six
classy_ext.cython_directives = {'language_level': "3" if six.PY3 else "2"}

setup(
    name='classy_sz',
    version=VERSION,
    description='Python interface to the Cosmological Boltzmann code CLASS',
    url='http://www.class-code.net',
    cmdclass={'build_ext': build_ext},
    ext_modules=[classy_ext],
    #data_files=[('bbn', ['../bbn/sBBN.dat'])]
)
