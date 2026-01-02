
import os
import re

PLAYERS_DIR = "_players"

def fix_table_spacing(content):
    """Ensures a blank line exists before markdown tables."""
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Check if this line is a table header (e.g. | Header |)
        if line.strip().startswith('|') and '---' not in line:
             # Check if previous line is not empty and not a table part
             if i > 0 and lines[i-1].strip() != '' and not lines[i-1].strip().startswith('|'):
                 new_lines.append('') # Add blank line
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def apply_skills_grid(content):
    """Splits skills into a 2-column grid."""
    
    # Locate Skills section
    skills_start = re.search(r'^##\s+Skills', content, re.MULTILINE)
    
    if not skills_start:
        return content
        
    start_pos = skills_start.end()
    
    # Find the start of the next main section (H2)
    next_section = re.search(r'^##\s+', content[start_pos:], re.MULTILINE)
    
    if next_section:
        end_idx = start_pos + next_section.start()
    else:
        end_idx = len(content)
    
    skills_content = content[start_pos:end_idx].strip()
    
    if "skills-grid" in skills_content:
        print("Skills grid already present, skipping.")
        return content
    
    # Split by H3 headers (Skills categories)
    # Pattern looks for "### Category Name" allowing for leading whitespace
    sections = re.split(r'(?=^\s*### )', skills_content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]
    
    if not sections:
        return content
        
    left_col = []
    right_col = []
    
    # Simple distribution: Alternating
    for i, section in enumerate(sections):
        if i % 2 == 0:
            left_col.append(section)
        else:
            right_col.append(section)
            
    # Construct new HTML
    new_skills_block = '\n<div class="skills-grid">\n  <div class="skills-col" markdown="1">\n\n'
    new_skills_block += '\n\n'.join(left_col)
    new_skills_block += '\n\n  </div>\n  <div class="skills-col" markdown="1">\n\n'
    new_skills_block += '\n\n'.join(right_col)
    new_skills_block += '\n\n  </div>\n</div>\n\n'
    
    new_content = content[:start_pos] + "\n" + new_skills_block + content[end_idx:]
    return new_content

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Update Layout
    content = re.sub(r'layout: page', 'layout: player', content)
    
    # 2. Fix Table Spacing
    content = fix_table_spacing(content)
    
    # 3. Apply Skills Grid
    content = apply_skills_grid(content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Processed {filepath}")

def main():
    if not os.path.exists(PLAYERS_DIR):
        print(f"Directory {PLAYERS_DIR} not found.")
        return

    for filename in os.listdir(PLAYERS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(PLAYERS_DIR, filename)
            process_file(filepath)

if __name__ == "__main__":
    main()
