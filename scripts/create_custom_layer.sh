#!/usr/bin/env bash

set -e

py_dir="$1/python"
rm -rf "${py_dir}"

mkdir -p "${py_dir}"
cp -pR "$2" "${py_dir}"

echo '{ "filename": "'"$1"'.zip", "source_dir": "'"$1"'" }'
