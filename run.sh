#!/bin/bash

# Campaign Tool Suite Interactive Menu

# Clear terminal screen
clear

echo "==============================================="
echo "      CYBERPUNK RED: CAMPAIGN TOOL SUITE       "
echo "==============================================="
echo "Select an operation to execute:"
echo ""

options=(
    "Reimport Obsidian Vault (Full site sync)"
    "Generate NotebookLM PDFs (Vault compilation)"
    "Standardize Lore Files (Obsidian source cleanup)"
    "Start Jekyll Dev Server (Local web preview)"
    "Build Jekyll Production Site (Verify build)"
    "Exit"
)

select opt in "${options[@]}"
do
    case $opt in
        "Reimport Obsidian Vault (Full site sync)")
            echo ""
            echo "--> Running Reimport Pipeline..."
            bash scripts/import_obsidian.sh
            echo "--> Reimport completed."
            break
            ;;
        "Generate NotebookLM PDFs (Vault compilation)")
            echo ""
            echo "--> Compiling campaign PDFs to NotebookLM..."
            python3 scripts/generate_pdf.py
            echo "--> PDF generation complete."
            break
            ;;
        "Standardize Lore Files (Obsidian source cleanup)")
            echo ""
            echo "--> Standardizing vault Lore files..."
            python3 scripts/standardize_lore.py
            echo "--> Lore standardization complete."
            break
            ;;
        "Start Jekyll Dev Server (Local web preview)")
            echo ""
            echo "--> Starting Jekyll development server..."
            bundle exec jekyll serve
            break
            ;;
        "Build Jekyll Production Site (Verify build)")
            echo ""
            echo "--> Building Jekyll static site..."
            bundle exec jekyll build
            echo "--> Build complete."
            break
            ;;
        "Exit")
            echo "Exiting Campaign Tool Suite. Stay frosty, choomba."
            exit 0
            ;;
        *)
            echo "Invalid selection. Please choose a number from 1 to ${#options[@]}."
            ;;
    esac
done
