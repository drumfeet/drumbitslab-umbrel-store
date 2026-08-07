#!/usr/bin/env bash
set -euo pipefail

blocked=()
while IFS= read -r -d '' path; do
  case "/$path/" in
    */.env.example/)
      ;;
    */.env/|*/.env.*/*|*/data/*|*/local-data/*|*/artifacts/*|*/screenshots/*)
      blocked+=("$path")
      ;;
  esac
done < <(git ls-files -z)

if ((${#blocked[@]})); then
  printf 'Refusing to publish tracked runtime or secret files:\n' >&2
  printf -- '- %s\n' "${blocked[@]}" >&2
  exit 1
fi

echo "Public catalog check passed."
