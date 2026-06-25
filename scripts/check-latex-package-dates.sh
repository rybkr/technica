#!/bin/sh
set -eu

today=$(date +%Y/%m/%d)
failed=0

changed_files=$(git diff --cached --name-only --diff-filter=AM -- '*.sty')

if [ -z "$changed_files" ]; then
    exit 0
fi

for path in $changed_files; do
    provides_line=$(git show ":$path" | sed -n '1,20{/\\ProvidesPackage{/p;}')

    if [ -z "$provides_line" ]; then
        printf '%s\n' "error: $path is staged but has no \\ProvidesPackage line near the top." >&2
        failed=1
        continue
    fi

    package_date=$(printf '%s\n' "$provides_line" | sed -n 's/.*\[\([0-9][0-9][0-9][0-9]\/[0-9][0-9]\/[0-9][0-9]\).*/\1/p')

    if [ -z "$package_date" ]; then
        printf '%s\n' "error: $path has a \\ProvidesPackage line without a YYYY/MM/DD date." >&2
        failed=1
        continue
    fi

    if [ "$package_date" != "$today" ]; then
        printf '%s\n' "error: $path has package date $package_date, expected $today for this commit." >&2
        failed=1
    fi
done

if [ "$failed" -ne 0 ]; then
    printf '%s\n' "Update the date in each staged \\ProvidesPackage line, then stage the file again." >&2
    exit 1
fi
