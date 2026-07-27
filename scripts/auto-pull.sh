#!/usr/bin/env bash
# ============================================================
#  auto-pull.sh
#  Detecta mudanças remotas e faz pull automático antes de push.
#  Evita o vai-e-vem de conflitos quando você edita pelo GitHub Web.
#
#  Uso:
#    ./auto-pull.sh                     # verifica e faz pull se houver mudanças
#    ./auto-pull.sh --push "mensagem"   # depois de pullar, commita e dá push
# ============================================================
set -e

PUSH_MSG="${1:-chore: update via auto-pull}"

# 1. Verifica se é repo git
if [ ! -d ".git" ]; then
  echo "❌ Não é um repositório git. Rode dentro da pasta do projeto."
  exit 1
fi

# 2. Confirma que tem remote origin
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "❌ Sem remote 'origin' configurado."
  exit 1
fi

# 3. Identifica a branch atual
BRANCH=$(git branch --show-current)
echo "🌿 Branch atual: $BRANCH"

# 4. Fetch (sem merge) — só descobre se há mudanças remotas
echo "🔍 Verificando mudanças remotas..."
git fetch origin "$BRANCH" 2>&1 | tail -3

# 5. Compara local vs. remoto
LOCAL=$(git rev-parse "$BRANCH")
REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "$LOCAL")

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "✅ Local e remoto estão em sincronia. Nada para puxar."
else
  echo "🔄 Mudanças detectadas no remoto. Fazendo pull com rebase..."

  # Tenta stash se houver mudanças locais não-comitadas
  NEEDS_STASH=false
  if ! git diff-index --quiet HEAD --; then
    echo "📦 Você tem mudanças não-comitadas. Fazendo stash..."
    git stash push -m "auto-pull: stash temporário"
    NEEDS_STASH=true
  fi

  # Pull com rebase
  if git pull --rebase origin "$BRANCH" 2>&1; then
    echo "✅ Pull realizado com sucesso."

    # Restaura stash se necessário
    if [ "$NEEDS_STASH" = "true" ]; then
      echo "📦 Restaurando suas mudanças do stash..."
      git stash pop || echo "⚠️  Conflito no stash. Resolva manualmente com: git stash pop"
    fi
  else
    echo "❌ Conflito durante o rebase. Resolva manualmente:"
    echo "   1. Edite os arquivos com conflito"
    echo "   2. git add <arquivo-resolvido>"
    echo "   3. git rebase --continue"
    echo "   4. Rode este script de novo"
    if [ "$NEEDS_STASH" = "true" ]; then
      echo "📦 Restaurando seu stash (pode dar conflito):"
      git stash pop || true
    fi
    exit 1
  fi
fi

# 6. Push opcional (se passado como argumento)
if [ "$1" = "--push" ] || [ -n "$1" ]; then
  if git diff-index --quiet HEAD --; then
    echo "ℹ️  Sem mudanças locais para comitar."
  else
    echo "💾 Commitando mudanças locais..."
    git add -A
    git commit -m "$PUSH_MSG" 2>&1 | tail -3
  fi

  echo "🚀 Fazendo push..."
  git push -u origin "$BRANCH" 2>&1 | tail -5
fi

# 7. Resumo final
echo ""
echo "=== STATUS FINAL ==="
git log --oneline | head -5
echo ""
git status --short
echo ""
echo "✅ Pronto!"
