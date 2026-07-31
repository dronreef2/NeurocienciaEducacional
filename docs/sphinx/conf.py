# ============================================
# docs/sphinx/conf.py
# Configuração do Sphinx para documentação
# ============================================

# -- Project information -------------------------------------------------
project = 'Neurociencia Educacional'
author = 'Programa de Pesquisa (UFRN/CERES)'
copyright = f'2026, {author}'

# -- General configuration -------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'myst_parser',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 4,
    'display_version': True,
}

# -- Options for LaTeX/PDF output -------------------------------------------
latex_engine = 'pdflatex'

# -- Intersphinx mappings ---------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'mne': ('https://mne.tools/mne-1.5/api.html', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
    'r': ('https://cran.r-project.org/doc/manuals/r-release/', None),
}

# -- Autodoc configuration --------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- MyST configuration -----------------------------------------------------
myst_enable_extensions = [
    'colon_fence',
    'dollarmath',
    'amsmath',
    'deflist',
    'fieldlist',
]

# -- Todo extension ---------------------------------------------------------
todo_include_todos = True
