import os
import re

# Directories to process
TARGET_DIRS = ["_corporations", "_people", "_players"]

def process_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    new_lines = []
    hidden_level = None # None means not hidden

    for line in lines:
        # Detect header
        header_match = re.match(r'^(#+)\s', line)
        
        if header_match:
            level = len(header_match.group(1))
            
            # Check if we are currently hidden
            if hidden_level is not None:
                # If new header is deeper (higher level), stay hidden
                if level > hidden_level:
                    continue
                else:
                    # New header is same or higher up (lower level), so potential to unhide
                    hidden_level = None
            
            # Check if this new header is start of a secret section
            if "#secret" in line or "GM Notes" in line:
                hidden_level = level
                continue # Don't write this line
                
        # Non-header line
        else:
            if hidden_level is not None:
                continue
        
        new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    print(f"Processed secrets in {filepath}")

def main():
    base_dir = "." # Assumes running from root
    
    for folder in TARGET_DIRS:
        dir_path = os.path.join(base_dir, folder)
        if not os.path.exists(dir_path):
             print(f"Skipping {folder}, does not exist.")
             continue
             
        for filename in os.listdir(dir_path):
            if filename.endswith(".md"):
                process_file(os.path.join(dir_path, filename))

if __name__ == "__main__":
    main()
