import os
import re
import yaml

TARGET_DIRS = ["_corporations", "_people", "_players", "_lore", "_session_recaps"]

def build_file_map():
    file_map = {} # Maps title or filename to relative path (e.g., _people/Name.md)
    
    for folder in TARGET_DIRS:
        if not os.path.exists(folder):
            continue
            
        for filename in os.listdir(folder):
            if filename.endswith(".md"):
                path = os.path.join(folder, filename)
                name_no_ext = os.path.splitext(filename)[0]
                
                # Add filename to map
                file_map[name_no_ext.lower()] = path
                
                # Try to extract title from front matter
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.startswith('---'):
                            parts = content.split('---')
                            if len(parts) >= 3:
                                front_matter = yaml.safe_load(parts[1])
                                if front_matter and 'title' in front_matter:
                                    file_map[front_matter['title'].lower()] = path
                                if front_matter and 'name' in front_matter:
                                    file_map[front_matter['name'].lower()] = path
                except Exception as e:
                    print(f"Error reading {path}: {e}")
                    
    return file_map

def resolve_links_in_content(content, file_map):
    def replace_link(match):
        full_match = match.group(0)
        link_target = match.group(1).strip()
        alias = match.group(3).strip() if match.group(3) else None
        
        target_key = link_target.lower()
        
        if target_key in file_map:
            target_path = file_map[target_key]
            display_text = alias if alias else link_target
            return f"[{display_text}]({{% link {target_path} %}})"
        else:
            # If not found, just return the text without brackets (or with if we want to see it's missing)
            # For now, let's just return the text as requested by the user's observation
            return alias if alias else link_target

    # Pattern for [[Link]] or [[Link|Alias]]
    pattern = r'\[\[([^\]|]+)(\|([^\]]+))?\]\]'
    return re.sub(pattern, replace_link, content)

def process_files(file_map):
    for folder in TARGET_DIRS:
        if not os.path.exists(folder):
            continue
            
        for filename in os.listdir(folder):
            if filename.endswith(".md"):
                path = os.path.join(folder, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = resolve_links_in_content(content, file_map)
                
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Resolved links in {path}")

def main():
    print("Building file map...")
    file_map = build_file_map()
    print(f"File map built with {len(file_map)} entries.")
    print("Resolving links...")
    process_files(file_map)
    print("Done.")

if __name__ == "__main__":
    main()
