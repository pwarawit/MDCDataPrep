from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'includes': ['sip','PyQt4'],
				#'bundle_files': 1,
				#'compressed': True,
				}},
    windows = [{'script': "main.py"}],
    zipfile = None,
)
