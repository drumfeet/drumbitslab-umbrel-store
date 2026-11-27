#!/usr/bin/env bash
set -euo pipefail

tracked_files=$(mktemp "${TMPDIR:-/tmp}/public-catalog.XXXXXX")
trap 'rm -f "$tracked_files"' EXIT
# Finish listing first so a Git failure cannot look like an empty catalog.
git ls-files -z > "$tracked_files"

blocked=()
while IFS= read -r -d '' path; do
  case "/$path/" in
    */data/*|*/local-data/*|*/artifacts/*|*/screenshots/*|*/tunnel/token/)
      blocked+=("$path")
      ;;
    */.env.example/)
      ;;
    */.env/|*/.env.*/*)
      blocked+=("$path")
      ;;
  esac
done < "$tracked_files"

if ((${#blocked[@]})); then
  printf 'Refusing to publish tracked runtime or secret files:\n' >&2
  printf -- '- %s\n' "${blocked[@]}" >&2
  exit 1
fi

echo "Public catalog check passed."
