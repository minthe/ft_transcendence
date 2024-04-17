#!/bin/bash

delete_migrations_contents() {
    local dir="$1"
    # Loop through all files and folders in the given directory
    for file in "$dir"/*; do
        if [[ -d "$file" ]]; then
            # If it's a directory
            if [[ "$(basename "$file")" == "migrations" ]]; then
                # If it's the migrations folder, delete its contents except __init__.py
                find "$file" -mindepth 1 -type f ! -name '__init__.py' -exec rm -f {} +
            else
                # Recursively call the function for subdirectories
                delete_migrations_contents "$file"
            fi
        fi
    done
}

# Start the deletion process from the current directory
delete_migrations_contents .

echo "Migrations contents deleted successfully."