import os
import re

LORE_DIR = "obsidian_vault/Lore"

def standardize_file(filepath):
    filename = os.path.basename(filepath)
    title_from_filename = os.path.splitext(filename)[0]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove existing front matter if present
    if content.strip().startswith('---'):
        parts = re.split(r'^---$', content.strip(), flags=re.MULTILINE)
        if len(parts) >= 3:
            content = '\n'.join(parts[2:]).strip()
    
    lines = content.split('\n')
    
    # 2. Identify the true title from the first H1 or filename
    original_title = title_from_filename
    first_header_idx = -1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            first_header_idx = i
            original_title = line.lstrip('#').strip()
            break
        elif line.startswith('### '): # Special case for 4th Corporate War
            first_header_idx = i
            original_title = line.lstrip('#').strip()
            break
            
    # 3. Clean the title (remove parenthetical years or common prefixes)
    clean_title = re.sub(r'\s*\(\d{4}[–-]?\d{0,4}\)', '', original_title)
    clean_title = re.sub(r'^Summary Recap of the\s+', '', clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r'^A History of the\s+', '', clean_title, flags=re.IGNORECASE)
    
    # 4. Construct new front matter
    front_matter = [
        "---",
        f"title: \"{clean_title}\"",
        "layout: lore",
        "---",
        ""
    ]
    
    # 5. Process Body
    new_body = []
    header_found = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Normalize the first header to a single # clean_title
        if (line.startswith('# ') or line.startswith('### ')) and not header_found:
            new_body.append(f"# {clean_title}")
            header_found = True
            continue
            
        # Normalize bold numeric headers: **1. Title** -> ## Title
        m_bold_num = re.match(r'^\*\*(\d+\.\s+)?(.*?)\*\*$', line_stripped)
        if m_bold_num:
            section_name = m_bold_num.group(2).strip()
            new_body.append(f"## {section_name}")
            continue
            
        # Normalize numeric H2 headers: ## 1. Title -> ## Title
        m_h2_num = re.match(r'^##\s+\d+\.\s+(.*)$', line)
        if m_h2_num:
            section_name = m_h2_num.group(1).strip()
            # If the name still has bold brackets like **Title**, remove them
            section_name = section_name.strip('*')
            new_body.append(f"## {section_name}")
            continue

        # Normalize H3 headers to H2 for consistency
        if line.startswith('### '):
            # If we already have a header_found but it was the very first H1, subheaders should be H2
            new_body.append(line.replace('### ', '## ', 1))
            continue
            
        new_body.append(line)
        
    # If no header was found, prepend one
    if not header_found:
        new_body.insert(0, f"# {clean_title}")
        new_body.insert(1, "")

    # Combine everything
    final_content = '\n'.join(front_matter + new_body)
    
    # Final cleanup: normalize multiple bank lines
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Standardized {filepath}")

def main():
    if not os.path.exists(LORE_DIR):
        print(f"Directory {LORE_DIR} not found.")
        return
        
    for filename in os.listdir(LORE_DIR):
        if filename.endswith(".md"):
            standardize_file(os.path.join(LORE_DIR, filename))

if __name__ == "__main__":
    main()
