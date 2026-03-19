import os

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

if __name__ == "__main__":
    SOURCE_DIRECTORY = "content"
    OUTPUT_FILE = "combined_content.md"
    
    # Ensure we are in the right directory or use absolute paths if needed
    # For now, we assume we're running from the project root.
    combine_markdown_files(SOURCE_DIRECTORY, OUTPUT_FILE)
