#!/bin/bash
# Incrémenter la version dans package.json

CURRENT=$(grep '"version"' package.json | grep -o '[0-9]*\.[0-9]*\.[0-9]*' | head -1)
MAJOR=$(echo $CURRENT | cut -d. -f1)
MINOR=$(echo $CURRENT | cut -d. -f2)
PATCH=$(echo $CURRENT | cut -d. -f3)
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

sed -i "s/\"version\": \"[0-9]*\.[0-9]*\.[0-9]*\"/\"version\": \"$NEW_VERSION\"/" package.json

echo "✅ Version mise à jour: $CURRENT → $NEW_VERSION"
