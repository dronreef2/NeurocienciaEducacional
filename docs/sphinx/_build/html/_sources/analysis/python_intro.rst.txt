================================
Análise em Python — Introdução
================================

Pipeline Python do programa.

Setup
=====

.. code-block:: bash

   pip install -r analise/requirements.txt
   # ou
   poetry install

Estrutura
=========

.. code-block:: text

   analise/Python/
   ├── neurociencia_edu/        # Package source
   │   ├── __init__.py
   │   ├── eeg/
   │   │   ├── preprocessing.py
   │   │   └── erp.py
   │   ├── stats/
   │   │   └── mediation.py
   │   ├── io/
   │   │   └── bids.py
   │   └── tests/
   │       └── test_package.py
   ├── notebooks/               # Jupyter
   │   ├── 01_eeg_exploration.ipynb
   │   ├── 02_erp_statistics.ipynb
   │   └── 03_complete_workflow.ipynb
   └── dashboard/               # Streamlit
       ├── app.py
       └── pages/

Módulos principais
==================

- ``neurociencia_edu.eeg.preprocessing`` — MNE preprocessing
- ``neurociencia_edu.eeg.erp`` — ERP analysis
- ``neurociencia_edu.stats.mediation`` — Análise de mediação
- ``neurociencia_edu.io.bids`` — BIDS dataset

Como usar
=========

.. code-block:: python

   from neurociencia_edu.eeg import preprocess_subject
   from neurociencia_edu.stats import mediation_analysis

   # Pré-processar EEG
   preprocess_subject(
       input_path="dados/raw/P03/subj01.vhdr",
       output_root="dados/processed/P03",
       projeto="P03",
   )

   # Análise de mediação
   result = mediation_analysis(X, M, Y)
   print(f"Efeito indireto: {result.indirect:.3f}")
   print(f"IC 95%: [{result.ci_lower:.3f}, {result.ci_upper:.3f}]")
