#!/bin/bash

# Function to get the latest migration version
get_latest_migration_version() {
  local migration_folder="$1"
  local max_version=0

  # Loop over each .sql file in the migration folder
  for file in "$migration_folder"/*.sql; do
    if [[ -f "$file" ]]; then
      # Extract the version from the filename (assuming format [timestamp]_[name]_[version].sql)
      filename=$(basename "$file")
      # Extract the version (we assume the format is timestamp_name_version.sql)
      version=$(echo "$filename" | sed -E 's/^[0-9]+_([a-zA-Z0-9_]+)_([0-9]+)_(up|down)\.sql$/\2/')

      # If a version is found and it's greater than the current max_version, update max_version
      if [[ "$version" =~ ^[0-9]+$ ]]; then
        if [ "$version" -gt "$max_version" ]; then
          max_version=$version
        fi
      fi
    fi
  done

  # Return the highest version found
  echo $max_version
}

# Function to create a new migration
new_migration() {
  local name="$1"
  local path="./migrations"
  
  # Ensure the migrations directory exists
  mkdir -p "$path"

  # Get the latest migration version and calculate the next one
  local latest_version=$(get_latest_migration_version $path)
  local migration_version="$((latest_version + 1))"

  # Get the current Unix timestamp
  local timestamp=$(date +%s)

  # Construct the filename
  local filename="${timestamp}_${name}_${migration_version}"

  # Create the _up.sql and _down.sql files
  echo "-- Write migration here." > "$path/${filename}_up.sql"
  echo "-- Write migration rollback here." > "$path/${filename}_down.sql"

  echo "Migration created: $path/${filename}_up.sql and $path/${filename}_down.sql"
}

# Main logic to handle command-line arguments
if [ "$1" == "new" ] && [ -n "$2" ]; then
  # Call the new_migration function with the provided name argument
  new_migration "$2"
else
  echo "Usage: migrations new [name]"
  exit 1

fi
