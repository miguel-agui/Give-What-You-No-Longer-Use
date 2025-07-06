#!/bin/bash

# 📦 Script de sincronización manual entre entornos Git
# Autor: Jesús Abregú
# Fecha: 5 de julio 2025

OLD_PATH="$HOME/Give-OLD"
CURRENT_PATH="$HOME/Give-What-You-No-Longer-Use"

echo "🔁 Iniciando sincronización desde $OLD_PATH a $CURRENT_PATH ..."
echo "🧼 Excluyendo .git para evitar conflictos de historial"

rsync -av --exclude='.git' "$OLD_PATH/" "$CURRENT_PATH/"

echo "✅ Sincronización completada."

cd "$CURRENT_PATH" || exit

echo "🔍 Verificando estado del repositorio..."
git status

read -p "¿Deseás agregar y commitear los cambios? (s/n): " RESP
if [[ "$RESP" == "s" || "$RESP" == "si" ]]; then
if [[ "$RESP" =~ ^[sS](i)?$ ]]; then

    git add .
    git commit -m "Merge manual desde entorno Give-OLD: sincronización de archivos clave"
    git push origin abjes/setup-entorno-inicial
    echo "🚀 Cambios subidos con éxito."
else
    echo "📌 Cambios no commitados. Revisión manual pendiente."
fi

