import os
import re
import yaml

SOURCE_FILE = "obsidian_vault/Details Tables/Corporate Levels.md"
TARGET_FILE = "_data/corporate_levels.yml"

def process_levels(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Split into sections based on headers "### **#. Label**"
        sections = re.split(r'### \*\*\d+\.\s+(.*?)\*\*', content)[1:]

        data = {}

        # sections is a list: [label1, content1, label2, content2, ...]
        for i in range(0, len(sections), 2):
            raw_label = sections[i].strip()
            
            # Label might have extra info: "Security (Defensive Hardware & Personnel)"
            # Let's extract just the base label to match our Discovered Details labels
            label_match = re.match(r'^([^\(]+)', raw_label)
            if label_match:
                label = label_match.group(1).strip()
            else:
                label = raw_label
            
            section_content = sections[i+1]
            
            # Map of values: {0: "", 1: "", ...}
            levels_map = {}

            # Parse lines like "- **0-1: Negligent.** Description..." or "- **10: Fortress.** Description..."
            items = re.findall(r'-\s+\*\*(.*?)\*\*(.*)', section_content)
            
            for range_str, description in items:
                desc = description.strip()
                # Parse range "0-1:" or "10: Fortress." -> Need to split out the string part
                # e.g "0-1: Negligent." or "10: Fortress."
                # We split on colon if present
                clean_range_text = range_str.split(':')[0].strip()
                
                parts = clean_range_text.split('-')
                if len(parts) == 2:
                    start_val = int(parts[0])
                    end_val = int(parts[1])
                    for val in range(start_val, end_val + 1):
                        levels_map[val] = f"**{range_str}** {desc}"
                elif len(parts) == 1:
                    val = int(parts[0])
                    levels_map[val] = f"**{range_str}** {desc}"

            data[label] = levels_map
        
        # Ensure _data directory exists
        os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)

        with open(TARGET_FILE, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
            
        print(f"Successfully created {TARGET_FILE}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    if not os.path.exists(SOURCE_FILE):
        print(f"Source file {SOURCE_FILE} not found.")
    else:
        process_levels(SOURCE_FILE)
