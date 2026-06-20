import os
import re
import yaml

TARGET_DIRS = ["_corporations", "_people", "_players", "_lore", "_session_recaps", "_missions"]

# Maps target_path to its clean title or name
path_title_map = {}

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
                                if front_matter:
                                    title = front_matter.get('name') or front_matter.get('title')
                                    if title:
                                        path_title_map[path] = title
                                        file_map[title.lower()] = path
                except Exception as e:
                    print(f"Error reading {path}: {e}")
                    
    return file_map

def resolve_links_in_frontmatter(content, file_map):
    def replace_link(match):
        link_target = match.group(1).strip()
        alias = match.group(3).strip() if match.group(3) else None
        
        target_key = link_target.lower()
        
        if target_key in file_map:
            target_path = file_map[target_key]
            display_text = alias if alias else path_title_map.get(target_path, link_target)
            
            # Format target_path (e.g., _missions/File.md) to URL (e.g., /missions/File.html)
            parts = target_path.split(os.sep)
            if len(parts) >= 2:
                collection = parts[0].lstrip('_')
                filename = os.path.splitext(parts[1])[0]
                url = f"/{collection}/{filename}.html"
            else:
                url = f"/{target_path.lstrip('_').replace('.md', '.html')}"
                
            return f"[{display_text}]({url})"
        else:
            return alias if alias else link_target

    pattern = r'\[\[([^\]|]+)(\|([^\]]+))?\]\]'
    return re.sub(pattern, replace_link, content)

def resolve_links_in_body(content, file_map):
    def replace_link(match):
        link_target = match.group(1).strip()
        alias = match.group(3).strip() if match.group(3) else None
        
        target_key = link_target.lower()
        
        if target_key in file_map:
            target_path = file_map[target_key]
            display_text = alias if alias else path_title_map.get(target_path, link_target)
            return f"[{display_text}]({{% link {target_path} %}})"
        else:
            return alias if alias else link_target

    pattern = r'\[\[([^\]|]+)(\|([^\]]+))?\]\]'
    return re.sub(pattern, replace_link, content)

def resolve_links_in_content(content, file_map):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            body = parts[2]
            
            resolved_fm = resolve_links_in_frontmatter(front_matter, file_map)
            resolved_body = resolve_links_in_body(body, file_map)
            
            return f"---{resolved_fm}---{resolved_body}"
            
    return resolve_links_in_body(content, file_map)

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
