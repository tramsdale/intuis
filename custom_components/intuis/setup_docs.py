import os
import subprocess
import sys
import shutil

def setup_docs():
    """Set up and build Sphinx documentation."""
    # Clean up existing docs directory if it exists
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    
    # Create fresh docs directory and source
    os.makedirs('docs/source')
    
    # Create index.rst
    with open('docs/source/index.rst', 'w') as f:
        f.write('''Welcome to IntuisNetatmo's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
''')
    
    # Create modules.rst
    with open('docs/source/modules.rst', 'w') as f:
        f.write('''API Documentation
===============

IntuisNetatmo
------------

.. automodule:: intuis_netatmo
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
''')
    
    # Create conf.py
    conf_content = '''# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'IntuisNetatmo'
copyright = '2024, Tim Ramsdale'
author = 'Tim Ramsdale'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx_autodoc_typehints'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
'''
    
    with open('docs/source/conf.py', 'w') as f:
        f.write(conf_content)
    
    # Create Makefile
    makefile_content = '''# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
'''
    
    with open('docs/Makefile', 'w') as f:
        f.write(makefile_content)
    
    # Build the documentation
    os.chdir('docs')
    subprocess.run(['make', 'html'])
    os.chdir('..')
    
    print("\nDocumentation has been built successfully!")
    print("You can view the documentation by opening docs/build/html/index.html in your browser.")

if __name__ == '__main__':
    setup_docs() 