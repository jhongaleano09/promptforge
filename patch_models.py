import os
import re

files_to_patch = [
    "backend/app/agents/nodes.py",
    "backend/app/agents/system_prompt_graph.py",
    "backend/app/agents/image_prompt_graph.py",
    "backend/app/agents/additional_prompt_graph.py"
]

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, "r") as f:
        content = f.read()

    # Find the block where selected_provider is assigned
    # And add selected_model
    content = re.sub(
        r'(selected_provider = state\.get\("selected_provider", None\))',
        r'\1\n        selected_model = state.get("selected_model", None)',
        content
    )

    # In clarify_node of nodes.py, selected_provider is assigned like this:
    content = re.sub(
        r'(# Obtener provider seleccionado si existe\s+selected_provider = state\.get\("selected_provider", None\))',
        r'\1\n        selected_model = state.get("selected_model", None)',
        content
    )
    
    # In some places, selected_provider is used but not explicitly assigned from state just before get_active_api_key.
    # Actually, let's just do a blanket replace for the model assignment.
    # Instead of doing it nicely, I can just replace `model=api_key_info['model_preference']`
    # with `model=state.get("selected_model") or api_key_info['model_preference']`!
    # This is much safer and simpler.
    
    content = re.sub(
        r"model=api_key_info\['model_preference'\]",
        r"model=state.get('selected_model') or api_key_info['model_preference']",
        content
    )
    
    with open(filepath, "w") as f:
        f.write(content)
        
    print(f"Patched {filepath}")

