directories=(
  "/home/osint/Desktop/TestingFolder/"
  "/home/osint/Desktop/TestingFolder/2"
)

for dir in "${directories[@]}"; do

  echo "Checking directory: ${dir}"
  if [[ ! -d "$dir" ]]; then
    echo "Directory ${dir} does not exist"
    continue
  fi
  
  find "$dir" -type f -size +5M -print0 | while IFS= read -r -d '' file; do
    if [[ "$file" =~ \.old[0-9]*$ ]]; then
      echo "Skipping ${file} already has .old"
      continue
    fi
    
    base_name=$(basename "$file")
    new_name="${file}.old"
    i=1
    
    while [[ -e "$new_name" || -L "$new_name" ]]; do
      new_name="${file}.old${i}"
      ((i++))
    done
    mv "$file" "$new_name"
    echo "Renammed ${file} to ${new_name}"
  done
done

