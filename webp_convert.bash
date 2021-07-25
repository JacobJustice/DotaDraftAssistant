#!/bin/bash

for filename in data/webp_portraits/*.webp; do
    dwebp "$filename" -o "./data/portraits/$(basename "$filename" .webp).png"
done

