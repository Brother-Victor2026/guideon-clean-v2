#!/bin/bash
cd ~/my-ai

# Lire la version actuelle
CURRENT=$(grep '"version"' package.json | grep -oP '\d+\.\d+\.\d+')

# Incrémenter le patch
NEW_VERSION=$(echo $CURRENT | awk -F. '{$NF=$NF+1; print $1"."$2"."$3}')

# Mettre à jour package.json
sed -i "s/\"version\": \"$CURRENT\"/\"version\": \"$NEW_VERSION\"/" package.json

# Mettre à jour .last-version AVEC LA NOUVELLE VERSION
echo "$NEW_VERSION" > .last-version

echo "✅ Version: $CURRENT → $NEW_VERSION"
