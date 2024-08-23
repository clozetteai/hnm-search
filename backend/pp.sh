#!/bin/zsh

for file in assets/*_compressed.jpg; do
  mv "$file" "${file/_compressed/}"
done

