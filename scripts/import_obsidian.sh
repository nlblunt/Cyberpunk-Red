#!/bin/bash

# Configuration
VAULT_DIR="obsidian_vault"
SITE_DIR="."

# Check if vault exists
if [ ! -d "$VAULT_DIR" ]; then
    echo "Error: Obsidian vault not found at $VAULT_DIR"
    echo "Please create a symlink named 'obsidian_vault' pointing to your Obsidian vault."
    exit 1
fi

echo "Cleaning up old collections..."
rm -rf _corporations/* _people/* _players/* _lore/* _session_recaps/*

# Function to process and copy files
process_files() {
    local source_folder=$1
    local target_collection=$2
    
    echo "Processing $source_folder to $target_collection..."
    
    # Create target directory if it doesn't exist
    mkdir -p "$target_collection"
    
    # Find markdown files in source
    find "$VAULT_DIR/$source_folder" -name "*.md" | while read file; do
        filename=$(basename "$file")
        target_file="$target_collection/$filename"
        
        # Copy file
        cp "$file" "$target_file"
        
        # Ensure front matter exists
        if ! grep -q "^---" "$target_file"; then
             # Add default front matter if missing
             sed -i '1i---\nlayout: page\ntitle: '"${filename%.*}"'\n---\n' "$target_file"
        fi
        
        # Convert Wikilinks [[Link]] to [Link](/people/Link) - This is a simple approximation
        # We need a better strategy for linking between collections.
        # For now, let's just make them standard links and maybe we can fix paths later or use specific logic.
        # A common pattern: [[Target]] -> [Target]({{ site.baseurl }}/search/?q=Target) or try to guess.
        # For Cyberpunk Red specific:
        # [[Corporation Name]] -> [Corporation Name](/corporations/corporation-name)
        
        # Extract excerpt if present
        if grep -q "^# Excerpt" "$target_file"; then
            # Extract content between # Excerpt and the next header
            excerpt_content=$(sed -n '/^# Excerpt/,/^#/p' "$target_file" | sed '1d;$d' | tr -d '\n\r' | sed 's/"/\\"/g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            if [ -n "$excerpt_content" ]; then
                # Add to front matter (only after the FIRST ---)
                sed -i "0,/^---/s/^---/---\nexcerpt: \"$excerpt_content\"/" "$target_file"
                # Remove the excerpt section from the file body
                # This sed command deletes from # Excerpt up to (but not including) the next # header
                sed -i '/^# Excerpt/,/^#/ { /^#/!d; /^# Excerpt/d }' "$target_file"
            fi
        fi
        
        # Normalize dates if present
        for date_field in "real_date" "in_game_date"; do
            if grep -q "^$date_field:" "$target_file"; then
                date_val=$(grep "^$date_field:" "$target_file" | cut -d':' -f2- | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr -d '"'\')
                # Check for MM/DD/YYYY or MM-DD-YYYY
                if echo "$date_val" | grep -qE "^[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}$"; then
                    # Convert to YYYY-MM-DD
                    m=$(echo "$date_val" | cut -d'/' -f1 | cut -d'-' -f1)
                    d=$(echo "$date_val" | cut -d'/' -f2 | cut -d'-' -f2)
                    y=$(echo "$date_val" | cut -d'/' -f3 | cut -d'-' -f3)
                    # Padding
                    [ ${#m} -eq 1 ] && m="0$m"
                    [ ${#d} -eq 1 ] && d="0$d"
                    new_date="$y-$m-$d"
                    sed -i "s/^$date_field:.*/$date_field: $new_date/" "$target_file"
                fi
            fi
        done
        
        # Basic replacement: [[Link|Alias]] -> Alias, then [[Link]] -> Link
        # DEPRECATED: Stripping brackets is now handled by resolve_links.py which converts them to Jekyll links.
        # sed -i 's/\[\[[^]|]*|\([^]]*\)\]\]/\1/g' "$target_file"
        # sed -i 's/\[\[\([^]]*\)\]\]/\1/g' "$target_file"
        
        # Fix image paths (assumes images are in an 'attachments' folder or similar, might need adjustment)
        # sed -i 's/!\[\[\(.*\)\]\]/![\1](\/assets\/images\/\1)/g' "$target_file"
    done
}

# Function to enforce layout
enforce_layout() {
    local target_dir=$1
    local layout=$2
    
    echo "Enforcing layout $layout for $target_dir..."
    for file in "$target_dir"/*.md; do
        if grep -q "^layout:" "$file"; then
            sed -i "s/^layout:.*/layout: $layout/" "$file"
        else
            # Insert layout right after the first ---
            sed -i "0,/^---/s/^---/---\nlayout: $layout/" "$file"
        fi
    done
}

process_files "Corporations" "_corporations"
enforce_layout "_corporations" "corporation"
process_files "People" "_people"
enforce_layout "_people" "person"

process_files "Players" "_players"
# Player pages should probably use 'player' layout, checking if that's what we want
# enforce_layout "_players" "player"

process_files "Lore" "_lore"
enforce_layout "_lore" "lore"

process_files "Session Recaps" "_session_recaps"
enforce_layout "_session_recaps" "session_recap"

python3 scripts/resolve_links.py
python3 scripts/hide_secrets.py
python3 scripts/format_players.py

echo "Import complete."
