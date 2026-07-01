#!/bin/bash
set -eu

remove=
if [[ ${1:-} == "--remove" ]]; then
    remove=1
fi

script_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
store_dir="${HOME}/.cookiecutters"
mkdir -p "${store_dir}"

for directory in "${script_dir}/"*/; do
    name="$(basename "${directory}")"
    symlink="${store_dir}/sevaht-${name}"
    rm -f "${symlink}"
    if [[ -z ${remove} ]]; then
        ln -sf "${directory%*/}" "${symlink}"
    fi
done
