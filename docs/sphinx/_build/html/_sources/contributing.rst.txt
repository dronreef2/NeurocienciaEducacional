============
Contribuindo
============

Guia para contribuir com o programa.

Código de Conduta
=================

Este projeto segue o `Contributor Covenant`_ v1.4.

.. _Contributor Covenant: https://www.contributor-covenant.org/pt/version/1/4/code-of-conduct/

Como contribuir
===============

1. **Reportar bugs:** abrir uma issue
2. **Sugerir melhorias:** abrir uma issue
3. **Melhorar documentação:** abrir um PR
4. **Contribuir com código:** ver :ref:`setup`

Padrões de código
=================

R
^

- Estilo: `tidyverse style guide`_
- Lint: ``lintr::lint_dir()``
- Testes: ``testthat`` em ``analise/R/tests/``

.. _tidyverse style guide: https://style.tidyverse.org/

Python
^^^^^^

- Estilo: `PEP 8`_
- Lint: ``ruff check``
- Testes: ``pytest`` em ``analise/Python/neurociencia_edu/tests/``

.. _PEP 8: https://peps.python.org/pep-0008/

Commits
=======

Usamos `Conventional Commits`_ em **português**:

- ``feat:`` nova funcionalidade
- ``fix:`` correção
- ``docs:`` documentação
- ``analise:`` scripts
- ``protocolo:`` protocolos
- ``test:`` testes
- ``ci:`` CI/CD
- ``refactor:`` refatoração

.. _Conventional Commits: https://www.conventionalcommits.org/
