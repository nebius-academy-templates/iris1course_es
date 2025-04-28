for file in repos/*.zip; do
  [ -f "$file" ] && unzip "$file" -d repos
done
