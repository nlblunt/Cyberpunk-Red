import os
import re

CORP_DIR = "_corporations"

def process_file(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Regex to find "Discovered Details" section
        section_match = re.search(r'(## Discovered Details\n)(.*?)(?=\n## |\Z)', content, re.DOTALL)
        
        if not section_match:
            return

        details_block = section_match.group(2)
        
        details_list = []
        lines = details_block.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            is_unknown = '#unknown' in line
            # Remove #unknown to clean up parsing
            clean_line = line.replace('#unknown', '').strip()
            
            # Robust parsing
            # Matches: - Label(:) Val/Max (- Note)
            m = re.match(r'-\s+(.*?)(?::)?\s+(\d+)/(\d+)(?:[\s-]+(.+))?$', clean_line)
            
            if m: 
                label = m.group(1).replace('*', '').strip()
                val_captured = int(m.group(2))
                max_val = int(m.group(3))
                note = m.group(4)
                if note: note = note.strip()
                else: note = ""

                if is_unknown:
                    final_value = 0
                    final_note = ""
                else:
                    final_value = val_captured
                    final_note = note

                details_list.append({
                    'label': label,
                    'value': final_value,
                    'max': max_val,
                    'note': final_note,
                    'is_unknown': is_unknown
                })
        
        if not details_list:
            return

        # Construct YAML for frontmatter
        yaml_lines = ["discovered_details:"]
        for item in details_list:
            # Escape double quotes in strings
            label_safe = item['label'].replace('"', '\\"')
            note_safe = item['note'].replace('"', '\\"')
            
            yaml_lines.append(f"  - label: \"{label_safe}\"")
            yaml_lines.append(f"    value: {item['value']}")
            yaml_lines.append(f"    max: {item['max']}")
            yaml_lines.append(f"    note: \"{note_safe}\"")
            if item['is_unknown']:
                yaml_lines.append(f"    is_unknown: true")
        
        yaml_str = "\n".join(yaml_lines)
        
        # Remove the section from content but replace with Include tag for placement control
        content_no_section = content.replace(section_match.group(0), "{% include discovered_details.html %}\n\n")
        
        # Inject into frontmatter
        fm_match = re.match(r'^---\n(.*?)\n---', content_no_section, re.DOTALL)
        if fm_match:
            old_fm = fm_match.group(1)
            # Remove any existing discovered_details block from old_fm if we are re-running?
            # The script runs on the markdown file. If we run it multiple times, the section is already gone
            # and it won't find it again. That's fine.
            # But wait, import_obsidian copies fresh files every time. So we are always processing fresh files.
            
            new_fm = f"{old_fm}\n{yaml_str}"
            final_content = f"---\n{new_fm}\n---{content_no_section[fm_match.end():]}"
            
            with open(filepath, 'w') as f:
                f.write(final_content)
            print(f"Updated {filepath} with discovered details.")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(CORP_DIR):
        print(f"Directory {CORP_DIR} not found.")
        return

    for filename in os.listdir(CORP_DIR):
        if filename.endswith(".md"):
            process_file(os.path.join(CORP_DIR, filename))

if __name__ == "__main__":
    main()
