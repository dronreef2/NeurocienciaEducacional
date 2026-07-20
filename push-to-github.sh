#!/usr/bin/env bash
# ============================================================
#  push-to-github.sh
#  Sobe o programa de pesquisa para o GitHub.
#  Uso: ./push-to-github.sh <URL-do-repo>
#  Ex:  ./push-to-github.sh https://github.com/dronreef2/neurociencia-educacional.git
# ============================================================
set -e

REPO_URL="${1:-}"

if [ -z "$REPO_URL" ]; then
  echo "❌ Uso: $0 <URL-do-repo>"
  echo "   Ex: $0 https://github.com/dronreef2/neurociencia-educacional.git"
  exit 1
fi

# 1. Garantir que estamos num repo git
if [ ! -d ".git" ]; then
  echo "📦 Inicializando repositório git..."
  git init -b main
fi

# 2. Garantir que temos um commit
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "📝 Criando commit inicial..."
  git add .
  git -c user.name="Pesquisadora" -c user.email="pesquisadora@local" commit -m "feat: estrutura inicial do programa de pesquisa"
fi

# 3. Configurar remote
if git remote get-url origin >/dev/null 2>&1; then
  echo "🔄 Atualizando remote origin..."
  git remote set-url origin "$REPO_URL"
else
  echo "🔗 Adicionando remote origin..."
  git remote add origin "$REPO_URL"
fi

# 4. Renomear branch para main (padrão GitHub moderno)
git branch -M main

# 5. Push
echo "🚀 Enviando para $REPO_URL ..."
git push -u origin main

echo ""
echo "✅ Pronto! Acesse: ${REPO_URL%.git}"
echo ""
echo "📋 Próximos passos sugeridos:"
echo "  1. Confirmar visibilidade (público/privado) no GitHub"
echo "  2. Adicionar descrição + topics no repositório"
echo "  3. Convidar a Angela como colaboradora (Settings → Collaborators)"
echo "  4. Ativar GitHub Projects para o kanban"
echo "  5. Configurar branch protection rules na main"
