import re
from utils import client

def generate_recipe_suggestions(selected_ingredients):
    if not selected_ingredients:
        return []
    
    ingredients_list = [f"{count} {item}{'s' if count > 1 else ''}" 
                       for item, count in selected_ingredients.items()]
    ingredients_text = ", ".join(ingredients_list)
    
    recipe_prompt = f"""
Suggest exactly 5 simple recipe names using these ingredients: {ingredients_text}.
Recipes should:
1. Use 2-3 main ingredients
2. Assume common pantry staples
3. Cover different cuisines
4. Be practical for home cooking

Format as numbered list with PLAIN TEXT names only (no formatting):
1. Recipe 1
2. Recipe 2
...
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[recipe_prompt]
        )
        
        recipe_names = []
        for line in response.text.strip().split('\n'):
            if line.strip() and (line[0].isdigit() or line.startswith('-')):
                name = re.sub(r'^\d+[\.\-\)]\s*|^[\-\*]\s*', '', line).strip()
                name = re.sub(r'\*\*([^*]+)\*\*', r'\1', name)
                name = re.sub(r'\*([^*]+)\*', r'\1', name)
                name = re.sub(r'_([^_]+)_', r'\1', name)
                if name:
                    recipe_names.append(name)
        return recipe_names[:5]
    except Exception:
        return []

def generate_detailed_recipe(recipe_name, selected_ingredients):
    ingredients_list = [f"{count} {item}{'s' if count > 1 else ''}" 
                       for item, count in selected_ingredients.items()]
    ingredients_text = ", ".join(ingredients_list)
    
    detailed_prompt = f"""
Create a detailed recipe for "{recipe_name}" using: {ingredients_text}.

Structure the response with these exact sections:

**INGREDIENTS:**
List all ingredients needed, clearly marking which are available from the detected ingredients and which need to be added.

**PREP TIME:**
Preparation time in minutes

**COOK TIME:**
Cooking time in minutes

**EQUIPMENT NEEDED:**
List all kitchen tools and equipment required

**SERVING SIZE:**
Number of servings this recipe makes

**CALORIES:**
Approximate calories per serving

**INSTRUCTIONS:**
Provide clear, numbered step-by-step cooking instructions

**TIPS FOR SUCCESS:**
Helpful tips and variations for best results

Make sure each section is clearly separated and well-organized.
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[detailed_prompt]
        )
        return response.text
    except Exception:
        return "Error generating recipe"

def parse_recipe_sections(recipe_text):
    sections = {
        'ingredients': '',
        'prep_time': '',
        'cook_time': '',
        'equipment': '',
        'serving_size': '',
        'calories': '',
        'instructions': '',
        'tips': ''
    }
    
    current_section = None
    lines = recipe_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if '**INGREDIENTS:**' in line or 'INGREDIENTS:' in line:
            current_section = 'ingredients'
        elif '**PREP TIME:**' in line or 'PREP TIME:' in line:
            current_section = 'prep_time'
        elif '**COOK TIME:**' in line or 'COOK TIME:' in line:
            current_section = 'cook_time'
        elif '**EQUIPMENT NEEDED:**' in line or 'EQUIPMENT NEEDED:' in line:
            current_section = 'equipment'
        elif '**SERVING SIZE:**' in line or 'SERVING SIZE:' in line:
            current_section = 'serving_size'
        elif '**CALORIES:**' in line or 'CALORIES:' in line:
            current_section = 'calories'
        elif '**INSTRUCTIONS:**' in line or 'INSTRUCTIONS:' in line:
            current_section = 'instructions'
        elif '**TIPS FOR SUCCESS:**' in line or 'TIPS FOR SUCCESS:' in line:
            current_section = 'tips'
        elif current_section and not line.startswith('**'):
            if sections[current_section]:
                sections[current_section] += '\n' + line
            else:
                sections[current_section] = line
    
    return sections