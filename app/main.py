import gradio as gr
import os
import shutil
import re
from food_detection import capture_image, detect_food_items, count_food_items, create_annotated_image
from recipe_generation import generate_recipe_suggestions, generate_detailed_recipe, parse_recipe_sections
from theme import CoolTheme
from templates import header_template, recipe_section_template, time_template, serving_template

with open("./static/styles.css", "r") as f:
    css = f.read()

def process_image(image_path):
    annotations = detect_food_items(image_path)
    if not annotations:
        return image_path, gr.CheckboxGroup(choices=[], value=[]), "No ingredients detected"
    
    food_counts = count_food_items(annotations)
    if not food_counts:
        return image_path, gr.CheckboxGroup(choices=[], value=[]), "No valid ingredients found"
    
    choices = [f"{item.title()} ({count})" for item, count in food_counts.items()]
    annotated_path = create_annotated_image(image_path, annotations) or image_path
    
    return annotated_path, gr.CheckboxGroup(choices=choices, value=[]), "Ingredients detected"

def capture_and_detect():
    image_path = "data/captured.jpg"
    if not capture_image(image_path):
        return None, gr.CheckboxGroup(choices=[], value=[]), "Camera error"
    return process_image(image_path)

def upload_and_detect(file):
    if not file:
        return None, gr.CheckboxGroup(choices=[], value=[]), "Please upload an image"
    
    image_path = "data/uploaded.jpg"
    shutil.copy(file.name, image_path)
    return process_image(image_path)

def get_recipes(selected_ingredients):
    if not selected_ingredients:
        return "Please select ingredients", gr.Dropdown(choices=[], value=None)
    
    counts = {}
    for item in selected_ingredients:
        name = re.sub(r'\s*\(\d+\)$', '', item).lower()
        counts[name] = counts.get(name, 0) + 1
    
    recipes = generate_recipe_suggestions(counts)
    if not recipes:
        return "No recipes generated", gr.Dropdown(choices=[], value=None)
    
    recipe_list = "\n".join([f"{i+1}. {r}" for i, r in enumerate(recipes)])
    return recipe_list, gr.Dropdown(choices=recipes, value=None)

def show_recipe_details(recipe_name, selected_ingredients, serving_size):
    if not recipe_name:
        return ("", "", "", "", "", "")
    
    counts = {}
    for item in selected_ingredients:
        name = re.sub(r'\s*\(\d+\)$', '', item).lower()
        counts[name] = counts.get(name, 0) + 1
    
    detailed_recipe = generate_detailed_recipe(recipe_name, counts, serving_size)
    sections = parse_recipe_sections(detailed_recipe)
    
    ingredients_html = recipe_section_template(
        "ingredients", 
        sections['ingredients'].replace('\n', '<br>'), 
        "🥗"
    )
    
    time_html = recipe_section_template(
        "time", 
        time_template(sections['prep_time'], sections['cook_time']), 
        "⏱️"
    )
    
    equipment_html = recipe_section_template(
        "equipment", 
        sections['equipment'].replace('\n', '<br>'), 
        "🔧"
    )
    
    serving_html = recipe_section_template(
        "serving", 
        serving_template(sections['serving_size'], sections['calories']), 
        "🍽️"
    )
    
    instructions_html = recipe_section_template(
        "instructions", 
        sections['instructions'].replace('\n', '<br>'), 
        "📝"
    )
    
    tips_html = recipe_section_template(
        "tips", 
        sections['tips'].replace('\n', '<br>'), 
        "💡"
    )
    
    return (ingredients_html, time_html, equipment_html, 
            serving_html, instructions_html, tips_html)

with gr.Blocks(theme=CoolTheme(), css=css) as demo:
    with gr.Column(elem_classes=["main"]):
        gr.Markdown(header_template())
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🖼️ Image Source", elem_classes=["section-header"])
                with gr.Row():
                    capture_btn = gr.Button("📸 Capture Image", variant="primary", elem_classes=["btn-primary"])
                    upload_btn = gr.UploadButton("📁 Upload Image", file_types=["image"], elem_classes=["btn-secondary"])
                status = gr.Textbox(label="Status", interactive=False, elem_classes=["status-success"])
                
                gr.Markdown("### 🔍 Detected Ingredients", elem_classes=["section-header"])
                annotated_output = gr.Image(label="Food Detection", interactive=False, elem_classes=["image-container"])
            
            with gr.Column(scale=1):
                gr.Markdown("### 🥗 Selected Ingredients", elem_classes=["section-header"])
                ingredients_output = gr.CheckboxGroup(
                    label="Ingredients in your fridge", 
                    choices=[],
                    interactive=True,
                    elem_classes=["checkbox-group"]
                )
                
                with gr.Row():
                    generate_btn = gr.Button("🍳 Suggest Recipes", variant="primary", elem_classes=["btn-primary"])
                    serving_size = gr.Dropdown(
                        label="Serving Size", 
                        choices=[1, 2, 3, 4, 5, 6], 
                        value=2,
                        elem_classes=["dropdown"]
                    )
                
                gr.Markdown("### 📝 Recipe Suggestions", elem_classes=["section-header"])
                recipe_output = gr.Textbox(
                    label="Suggested Recipes", 
                    lines=4, 
                    interactive=False,
                    elem_classes=["text-content"]
                )
                
                with gr.Row():
                    recipe_selector = gr.Dropdown(
                        label="Choose a recipe to view details", 
                        choices=[],
                        interactive=True,
                        elem_classes=["dropdown"]
                    )
                    show_btn = gr.Button("👩‍🍳 Show Full Recipe", variant="primary", elem_classes=["btn-primary"])
        
        gr.Markdown("## 🍽️ Recipe Details", elem_classes=["section-header"])
        
        with gr.Column(elem_classes=["recipe-section"]):
            with gr.Row():
                ingredients_section = gr.HTML()
                time_section = gr.HTML()
            
            with gr.Row():
                equipment_section = gr.HTML()
                serving_section = gr.HTML()
            
            instructions_section = gr.HTML()
            tips_section = gr.HTML()

    capture_btn.click(
        capture_and_detect,
        inputs=[],
        outputs=[annotated_output, ingredients_output, status]
    )
    
    upload_btn.upload(
        upload_and_detect,
        inputs=[upload_btn],
        outputs=[annotated_output, ingredients_output, status]
    )
    
    generate_btn.click(
        get_recipes,
        inputs=[ingredients_output],
        outputs=[recipe_output, recipe_selector]
    )
    
    show_btn.click(
        show_recipe_details,
        inputs=[recipe_selector, ingredients_output, serving_size],
        outputs=[ingredients_section, time_section, equipment_section, serving_section, instructions_section, tips_section]
    )

if __name__ == "__main__":
    demo.launch(share=True)