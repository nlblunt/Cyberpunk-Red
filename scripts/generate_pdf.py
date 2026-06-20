import os
import re
import subprocess
import shutil

VAULT_DIR = "obsidian_vault"
NOTEBOOKLM_DIR = os.path.join(VAULT_DIR, "NotebookLM")
TEMP_HTML = "scratch/combined_document.html"

# CSS styling for a clean, professional book-style PDF
CSS_STYLE = """
<style>
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        margin: 40px;
    }
    h1 {
        font-size: 28px;
        color: #111;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-top: 40px;
        page-break-before: always;
    }
    h1.cover-title {
        font-size: 36px;
        text-align: center;
        margin-top: 150px;
        border-bottom: none;
        page-break-before: avoid;
    }
    h1.section-header {
        font-size: 32px;
        text-align: center;
        background-color: #f5f5f5;
        padding: 20px;
        border: 1px solid #ddd;
        margin-top: 100px;
    }
    h2 {
        font-size: 22px;
        color: #222;
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-top: 30px;
    }
    h3 {
        font-size: 18px;
        color: #444;
        margin-top: 20px;
    }
    p, li {
        font-size: 14px;
        color: #444;
    }
    ul {
        margin-bottom: 20px;
    }
    li {
        margin-bottom: 5px;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-size: 13px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    code {
        font-family: Consolas, Monaco, Courier, monospace;
        background-color: #f7f7f7;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 13px;
    }
    .cover-page {
        text-align: center;
        height: 100%;
        page-break-after: always;
    }
    .subtitle {
        font-size: 18px;
        color: #666;
        margin-top: 20px;
    }
    .meta {
        font-size: 12px;
        color: #999;
        margin-top: 200px;
    }
</style>
"""

def md_to_html(md_text):
    # Strip frontmatter
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) >= 3:
            md_text = parts[2]
            
    # Basic line-by-line parsing
    html_lines = []
    in_list = False
    in_table = False
    table_headers = None
    
    lines = md_text.split('\n')
    for line in lines:
        stripped = line.strip()
        
        # Table handling
        if stripped.startswith('|'):
            if not in_table:
                in_table = True
                html_lines.append('<table>')
            
            # Parse row
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(c.startswith('-') or c.startswith(':') for c in cells):
                # This is a separator line, skip it
                continue
                
            if not table_headers:
                table_headers = cells
                html_lines.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                html_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            continue
        elif in_table:
            in_table = False
            table_headers = None
            html_lines.append('</table>')
            
        # Header handling
        h_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if h_match:
            if in_list:
                in_list = False
                html_lines.append('</ul>')
            level = len(h_match.group(1)) + 1 # offset by 1 to keep hierarchy clean
            title = h_match.group(2)
            html_lines.append(f'<h{level}>{title}</h{level}>')
            continue
            
        # List handling
        list_match = re.match(r'^[\*\-\+]\s+(.*)$', line)
        if list_match:
            if not in_list:
                in_list = True
                html_lines.append('<ul>')
            item = list_match.group(1)
            html_lines.append(f'<li>{item}</li>')
            continue
        elif in_list and stripped == '':
            pass
        elif in_list and not list_match:
            in_list = False
            html_lines.append('</ul>')
            
        # Blank line
        if stripped == '':
            continue
            
        # Normal line
        # Escape HTML characters first
        safe_line = stripped.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html_lines.append(f'<p>{safe_line}</p>')
        
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')
        
    html_text = '\n'.join(html_lines)
    
    # Inline formatting
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_text)
    html_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_text)
    html_text = re.sub(r'`(.*?)`', r'<code>\1</code>', html_text)
    
    # Strip Obsidian Wikilinks [[Link|Alias]] -> Alias, [[Link]] -> Link
    html_text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', html_text)
    html_text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', html_text)
    
    # Format standard links as colored text without actual web link behavior in PDF
    html_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<span style="color: #2980b9; font-weight: bold;">\1</span>', html_text)
    
    return html_text

def gather_markdown_files(directory):
    files_list = []
    if not os.path.exists(directory):
        return files_list
        
    for root, dirs, files in os.walk(directory):
        # Sort to keep processing order consistent
        files.sort()
        for file in files:
            if file.endswith(".md"):
                files_list.append(os.path.join(root, file))
    return files_list

def generate_section_html(title, sections):
    html_content = []
    html_content.append("<!DOCTYPE html><html><head><meta charset='utf-8'>")
    html_content.append(CSS_STYLE)
    html_content.append("</head><body>")
    
    # Cover Page
    html_content.append("<div class='cover-page'>")
    html_content.append(f"<h1 class='cover-title'>{title}</h1>")
    html_content.append("<div class='subtitle'>Campaign Intelligence Report</div>")
    html_content.append("<div class='meta'>Generated from GM Vault Database</div>")
    html_content.append("</div>")
    
    for section_title, path in sections:
        if not os.path.exists(path):
            print(f"Skipping section: {section_title} (directory {path} not found)")
            continue
            
        print(f"  Compiling section: {section_title}...")
        html_content.append(f"<h1 class='section-header'>{section_title}</h1>")
        
        md_files = gather_markdown_files(path)
        for md_file in md_files:
            filename = os.path.basename(md_file)
            print(f"    Processing {filename}...")
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            clean_title = os.path.splitext(filename)[0]
            html_content.append(f"<h1>{clean_title}</h1>")
            html_content.append(md_to_html(content))
            
    html_content.append("</body></html>")
    return "\n".join(html_content)

def compile_pdf(title, sections, output_filename):
    print(f"Compiling PDF: {output_filename} ({title})...")
    
    # Generate temporary HTML
    html_text = generate_section_html(title, sections)
    with open(TEMP_HTML, 'w', encoding='utf-8') as f:
        f.write(html_text)
        
    # Convert HTML to PDF via LibreOffice
    try:
        cmd = [
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            TEMP_HTML,
            "--outdir", "."
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Move the output PDF to NotebookLM target folder
        generated_pdf = TEMP_HTML.replace(".html", ".pdf")
        generated_pdf_basename = os.path.basename(generated_pdf)
        dest_pdf = os.path.join(NOTEBOOKLM_DIR, output_filename)
        
        if os.path.exists(generated_pdf_basename):
            shutil.move(generated_pdf_basename, dest_pdf)
            
        print(f"Successfully generated PDF: {dest_pdf}")
    except Exception as e:
        print(f"Error compiling {output_filename}: {e}")

def main():
    os.makedirs("scratch", exist_ok=True)
    os.makedirs(NOTEBOOKLM_DIR, exist_ok=True)
    
    # Individual reports
    compile_pdf("Corporations Report", [("Corporations", os.path.join(VAULT_DIR, "Corporations"))], "_CORPORATIONS.pdf")
    compile_pdf("People Dossiers", [("People", os.path.join(VAULT_DIR, "People"))], "_PEOPLE.pdf")
    compile_pdf("Player Characters", [("Players", os.path.join(VAULT_DIR, "Players"))], "_PLAYERS.pdf")
    compile_pdf("Plot Outline & Operations", [("Plot", os.path.join(VAULT_DIR, "Plot"))], "_PLOT.pdf")
    compile_pdf("Session Recaps Log", [("Session Recaps", os.path.join(VAULT_DIR, "Session Recaps"))], "_SESSION RECAPS.pdf")
    
    # Cleanup temp HTML
    if os.path.exists(TEMP_HTML):
        os.remove(TEMP_HTML)
    print("All PDF compilations complete.")

if __name__ == "__main__":
    main()
