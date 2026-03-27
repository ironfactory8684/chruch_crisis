import os
import markdown
from xhtml2pdf import pisa

def combine_markdown_files(source_dir, output_file):
    # Get all .md files in the source directory
    files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
    # Sort files naturally (0. prologue, 01. chapter01, etc.)
    files.sort()
    
    print(f"Combining {len(files)} files found in {source_dir}...")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, filename in enumerate(files):
            filepath = os.path.join(source_dir, filename)
            print(f"Processing: {filename}")
            
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                # Add extra newlines and a thematic break between files
                if i < len(files) - 1:
                    outfile.write("\n\n---\n\n")
    
    print(f"Successfully created: {output_file}")

def convert_to_pdf(md_file, pdf_file):
    print(f"Converting {md_file} to {pdf_file}...")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML
    # Using 'extra' extension for tables, fences, etc.
    html_content = markdown.markdown(md_content, extensions=['extra', 'nl2br', 'sane_lists'])
    
    # Wrap in basic HTML structure with Korean font support for Mac
    full_html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <style>
            @font-face {{
                font-family: "KoreanFont";
                src: url("/System/Library/Fonts/Supplemental/AppleGothic.ttf");
            }}
            @page {{
                size: a4;
                margin: 2cm;
            }}
            body {{
                font-family: "KoreanFont", sans-serif;
                line-height: 1.6;
                font-size: 11pt;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 10px;
                border: 1px solid #ddd;
            }}
            hr {{
                border: 0;
                border-top: 1px solid #eee;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Export to PDF
    with open(pdf_file, "wb") as f:
        pisa_status = pisa.CreatePDF(full_html, dest=f)
    
    if pisa_status.err:
        print(f"Error during PDF conversion: {pisa_status.err}")
    else:
        print(f"Successfully created: {pdf_file}")

if __name__ == "__main__":
    SOURCE_DIRECTORY = "content"
    OUTPUT_MD = "combined_content.md"
    OUTPUT_PDF = "교회_mna시대를_해부하다.pdf"
    
    # 1. Combine MD files
    if os.path.exists(SOURCE_DIRECTORY):
        combine_markdown_files(SOURCE_DIRECTORY, OUTPUT_MD)
        
        # 2. Convert to PDF
        if os.path.exists(OUTPUT_MD):
            convert_to_pdf(OUTPUT_MD, OUTPUT_PDF)
    else:
        print(f"Error: Source directory '{SOURCE_DIRECTORY}' not found.")
