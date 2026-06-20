import os
import re
import yaml

MISSIONS_DIR = "_missions"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            print(f"Skipping {filepath}: No frontmatter found.")
            return

        front_matter_str = fm_match.group(1)
        body = content[fm_match.end():]

        try:
            front_matter = yaml.safe_load(front_matter_str)
        except Exception as e:
            print(f"Error parsing frontmatter in {filepath}: {e}")
            return

        # Check mission status
        status = front_matter.get('mission_status') or front_matter.get('status')
        if status not in ["In Progress", "Finished"]:
            print(f"Removing {filepath}: Status is '{status}' (not In Progress or Finished).")
            os.remove(filepath)
            return

        # Regex to find "Webpage Details" section
        # Matches: ## Webpage Details followed by content until the next ## header or end of file
        section_match = re.search(r'(## Webpage Details\n+)(.*?)(?=\n## |\Z)', body, re.DOTALL)
        
        if not section_match:
            print(f"Warning: {filepath} has no '## Webpage Details' section. Using blank content.")
            webpage_content = ""
        else:
            webpage_content = section_match.group(2).strip()

        # Update frontmatter to enforce layout: mission
        front_matter['layout'] = 'mission'
        
        new_fm_str = yaml.dump(front_matter, sort_keys=False).strip()
        
        final_content = f"---\n{new_fm_str}\n---\n\n{webpage_content}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Formatted mission {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(MISSIONS_DIR):
        print(f"Directory {MISSIONS_DIR} not found.")
        return

    for filename in os.listdir(MISSIONS_DIR):
        if filename.endswith(".md"):
            process_file(os.path.join(MISSIONS_DIR, filename))

if __name__ == "__main__":
    main()
