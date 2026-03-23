import os
import sys
import re
import json

# Function to generate documentation from docstrings
def generate_documentation():
    """Automatically generates project documentation from docstrings."""
    documentation = {}
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    docstring = re.search(r'"""(.*?)"""', content, re.DOTALL)
                    if docstring:
                        documentation[os.path.join(root, file)] = docstring.group(1).strip()
    with open('docs.json', 'w') as f:
        json.dump(documentation, f, indent=2)
    print('Documentation generated successfully!')

if __name__ == '__main__':
    generate_documentation()