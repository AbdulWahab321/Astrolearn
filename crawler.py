import os

def read_file_contents(filepath):
    """Reads and returns the contents of a file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    templates_dir = 'templates/'
    output_file = 'crawled.txt'
    extended_file_list = [r"C:\Users\jrabd\OneDrive\Documents\PYTHON_PROJECTS\AstroLearn\static\css\styles.css",r"C:\Users\jrabd\OneDrive\Documents\PYTHON_PROJECTS\AstroLearn\static\js\scripts.js"]  # Add your special files here

    # Ensure the templates directory exists
    if not os.path.exists(templates_dir):
        print(f"The directory {templates_dir} does not exist.")
        return

    # List all files in the templates directory
    files = [f for f in os.listdir(templates_dir) if os.path.isfile(os.path.join(templates_dir, f))]
    
    # Combine the files in templates directory with the extended file list
    all_files = files + extended_file_list

    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in all_files:
            filepath = os.path.join(templates_dir, filename) if filename in files else filename
            if os.path.exists(filepath):
                file_content = read_file_contents(filepath)
                output.write(f"{filename}: \n{file_content}\n")
            else:
                output.write(f"{filename}: File does not exist.\n")
                print(f"Warning: {filename} does not exist and will be skipped.")
    
    print(f"All file contents have been written to {output_file}")

if __name__ == "__main__":
    main()
