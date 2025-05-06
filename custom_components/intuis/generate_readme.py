import inspect
import re
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import intuis_netatmo

def get_function_docs(cls):
    """Extract function documentation from a class."""
    docs = []
    for name, member in inspect.getmembers(cls):
        if inspect.isfunction(member) and not name.startswith('_'):
            # Get function signature
            sig = inspect.signature(member)
            
            # Get return type
            return_type = sig.return_annotation
            if return_type == inspect.Parameter.empty:
                return_type_str = "None"
            else:
                return_type_str = return_type.__name__ if hasattr(return_type, '__name__') else str(return_type)
            
            # Get parameters
            params = []
            for param_name, param in sig.parameters.items():
                if param_name != 'self':
                    param_type = param.annotation
                    if param_type == inspect.Parameter.empty:
                        param_type_str = "Any"
                    else:
                        param_type_str = param_type.__name__ if hasattr(param_type, '__name__') else str(param_type)
                    params.append(f"{param_name}: {param_type_str}")
            
            # Get docstring
            doc = inspect.getdoc(member)
            if doc:
                # Split docstring into description and sections
                parts = doc.split('\n\n')
                description = parts[0]
                sections = {}
                current_section = None
                
                for line in doc.split('\n')[1:]:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith(':param '):
                        if 'Parameters' not in sections:
                            sections['Parameters'] = []
                        param_match = re.match(r':param (\w+): (.*)', line)
                        if param_match:
                            param_name, param_desc = param_match.groups()
                            sections['Parameters'].append(f"- `{param_name}`: {param_desc}")
                    elif line.startswith(':return:'):
                        sections['Returns'] = [line.replace(':return:', '').strip()]
                    elif line.startswith(':raises:'):
                        if 'Raises' not in sections:
                            sections['Raises'] = []
                        raises_match = re.match(r':raises (\w+): (.*)', line)
                        if raises_match:
                            exc_name, exc_desc = raises_match.groups()
                            sections['Raises'].append(f"- `{exc_name}`: {exc_desc}")
                
                # Format the documentation
                doc_lines = [description]
                for section, content in sections.items():
                    if content:
                        doc_lines.append(f"\n**{section}:**")
                        doc_lines.extend(content)
                
                doc = '\n'.join(doc_lines)
            
            docs.append({
                'name': name,
                'params': params,
                'return_type': return_type_str,
                'doc': doc
            })
    return docs

def generate_readme():
    """Generate the README.md file with function documentation."""
    try:
        # Get documentation for each class
        intuis_docs = get_function_docs(intuis_netatmo.IntuisNetatmo)
        room_docs = get_function_docs(intuis_netatmo.IntuisRoom)
        water_heater_docs = get_function_docs(intuis_netatmo.IntuisWaterHeater)
        
        # Generate README content
        readme_content = """# IntuisNetatmo

A Python library for controlling Netatmo smart thermostats and water heaters through the Intuis API.

## Installation

```bash
pip install intuis-netatmo
```

## Usage

```python
from intuis_netatmo import IntuisNetatmo

# Initialize the client
client = IntuisNetatmo(client_id="your_client_id", client_secret="your_client_secret")

# Authenticate
client.authenticate()

# Get rooms and water heaters
rooms = client.get_rooms()
water_heaters = client.get_water_heaters()
```

## API Reference

### IntuisNetatmo Class

"""
        # Add IntuisNetatmo class documentation
        for doc in intuis_docs:
            signature = f"{doc['name']}({', '.join(doc['params'])}) -> {doc['return_type']}"
            readme_content += f"\n#### `{signature}`\n\n"
            if doc['doc']:
                readme_content += f"{doc['doc']}\n\n"
        
        readme_content += "\n### IntuisRoom Class\n\n"
        
        # Add IntuisRoom class documentation
        for doc in room_docs:
            signature = f"{doc['name']}({', '.join(doc['params'])}) -> {doc['return_type']}"
            readme_content += f"\n#### `{signature}`\n\n"
            if doc['doc']:
                readme_content += f"{doc['doc']}\n\n"
        
        readme_content += "\n### IntuisWaterHeater Class\n\n"
        
        # Add IntuisWaterHeater class documentation
        for doc in water_heater_docs:
            signature = f"{doc['name']}({', '.join(doc['params'])}) -> {doc['return_type']}"
            readme_content += f"\n#### `{signature}`\n\n"
            if doc['doc']:
                readme_content += f"{doc['doc']}\n\n"
        
        # Write to README.md
        with open('README.md', 'w') as f:
            f.write(readme_content)
        
        print("README.md has been generated successfully!")
        
    except Exception as e:
        print(f"Error generating README: {str(e)}")

if __name__ == '__main__':
    generate_readme() 