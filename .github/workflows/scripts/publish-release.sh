#!/usr/bin/env bash
set -euo pipefail

: "${PACKAGE_NAME:?PACKAGE_NAME is required}"
: "${PACKAGE_VERSION:?PACKAGE_VERSION is required}"
: "${PACKAGE_PATH:?PACKAGE_PATH is required}"
: "${RELEASE_TAG:?RELEASE_TAG is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"

expected_tag="${PACKAGE_NAME}--v${PACKAGE_VERSION}"
if [[ "$RELEASE_TAG" != "$expected_tag" ]]; then
  echo "Tag $RELEASE_TAG diverge de $expected_tag" >&2
  exit 1
fi

if git rev-parse --verify --quiet "refs/tags/${RELEASE_TAG}^{commit}" >/dev/null; then
  tag_sha=$(git rev-list -n 1 "$RELEASE_TAG")
  if [[ "$tag_sha" != "$GITHUB_SHA" ]]; then
    echo "Tag imutável $RELEASE_TAG já aponta para $tag_sha, não para $GITHUB_SHA" >&2
    exit 1
  fi
fi

metadata="${RUNNER_TEMP:-/tmp}/${PACKAGE_NAME}-${PACKAGE_VERSION}-release-metadata.json"
notes="${RUNNER_TEMP:-/tmp}/${PACKAGE_NAME}-${PACKAGE_VERSION}-notes.md"

python tools/release_metadata.py \
  --name "$PACKAGE_NAME" \
  --version "$PACKAGE_VERSION" \
  --path "$PACKAGE_PATH" \
  --tag "$RELEASE_TAG" \
  --sha "$GITHUB_SHA" \
  --repository "https://github.com/${GITHUB_REPOSITORY}" \
  --output "$metadata"

awk -v version="$PACKAGE_VERSION" '
  $0 ~ "^## \\[" version "\\]" { capture=1; next }
  capture && /^## / { exit }
  capture { print }
' "$PACKAGE_PATH/CHANGELOG.md" > "$notes"

if gh release view "$RELEASE_TAG" >/dev/null 2>&1; then
  gh release upload "$RELEASE_TAG" "$metadata" --clobber
  echo "Release $RELEASE_TAG já existia no SHA esperado; metadata reconciliada."
  exit 0
fi

if git rev-parse --verify --quiet "refs/tags/${RELEASE_TAG}^{commit}" >/dev/null; then
  gh release create "$RELEASE_TAG" "$metadata" \
    --verify-tag \
    --title "$PACKAGE_NAME $PACKAGE_VERSION" \
    --notes-file "$notes"
else
  gh release create "$RELEASE_TAG" "$metadata" \
    --target "$GITHUB_SHA" \
    --title "$PACKAGE_NAME $PACKAGE_VERSION" \
    --notes-file "$notes"
fi

