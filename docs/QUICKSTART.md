# 🚀 Quick Start — 5 minutos

> **Objetivo:** Clonar, instalar, rodar uma análise em 5 minutos.

## 1️⃣ Clonar o repositório (30s)

```bash
git clone https://github.com/dronreef2/NeurocienciaEducacional.git
cd NeurocienciaEducacional
```

## 2️⃣ Instalar dependências (1 min)

### Opção A: pip direto
```bash
pip install -r requirements.txt
pip install pandas numpy matplotlib scipy statsmodels networkx scikit-learn
```

### Opção B: Poetry (recomendado)
```bash
poetry install
poetry shell
```

### Opção C: Docker
```bash
docker build -f Dockerfile.dashboard -t neurociencia-dashboard .
docker run -p 8501:8501 neurociencia-dashboard
```

## 3️⃣ Validar dados (30s)

```bash
python3 analise/Python/scripts/validar_dados_piloto.py
```

Saída esperada:
```
✅ VALIDAÇÃO OK — 0 erros, 0 warnings
```

## 4️⃣ Gerar dados sintéticos (1 min)

```bash
python3 analise/Python/scripts/gerar_dados_sinteticos.py
```

Saída esperada:
```
✅ Todos os dados sintéticos gerados com sucesso!
```

## 5️⃣ Rodar análise (1 min)

```bash
# Análise do piloto
python3 analise/Python/scripts/analise_piloto_real.py

# Mixed models
python3 analise/Python/scripts/mixed_models_diarios.py
```

Saída: figuras em `resultados/` + relatórios JSON.

## 6️⃣ Dashboard (1 min para deploy)

Acesse: https://share.streamlit.io/

Preencha:
- Repository: `dronreef2/NeurocienciaEducacional`
- Branch: `main`
- Main file path: `streamlit_app.py`

Aguarde 2-5 min e abra: `https://neurociencia-educacional.streamlit.app`

## 🎯 Comandos essenciais

```bash
make help             # Lista comandos
make install         # Instalar tudo
make validate        # Validar dados
make test            # Rodar testes
make analyze-pilot   # Análise completa
make dashboard       # Dashboard local
make all             # Tudo
```

## 🐛 Problemas?

- **ImportError:** rode `pip install -r requirements.txt`
- **ModuleNotFoundError:** rode `pip install <modulo>`
- **Permission denied (SSH):** verifique chave SSH
- **Testes falhando:** rode `pip install pytest scipy statsmodels networkx`

## 📚 Próximos passos

1. 📖 Leia [USER-GUIDE.md](USER-GUIDE.md) para uso avançado
2. 🔬 Rode os [tutoriais Jupyter](../analise/Python/notebooks/)
3. 🌐 Explore o dashboard online
4. 📖 Veja [protocolos dos 5 projetos](../01-projeto-qualitativo-criancas-ia/protocolo/)
5. 🤝 Contribua via [CONTRIBUTING.md](../CONTRIBUTING.md)
