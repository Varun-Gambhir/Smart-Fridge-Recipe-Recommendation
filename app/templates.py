def header_template():
    return """
    <div style="text-align:center;">
        <h1 id="main-title">🍏 Smart Fridge Assistant 🥦</h1>
        <p class="subtitle">Capture your ingredients • Discover delicious recipes</p>
    </div>
    """

def recipe_section_template(section_type, content, icon):
    templates = {
        "ingredients": {
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "title": "Ingredients"
        },
        "time": {
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "title": "Time"
        },
        "equipment": {
            "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "title": "Equipment"
        },
        "serving": {
            "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
            "title": "Nutrition"
        },
        "instructions": {
            "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
            "title": "Instructions"
        },
        "tips": {
            "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
            "title": "Tips for Success"
        }
    }
    
    config = templates[section_type]
    
    if section_type == "time":
        return f"""
        <div style="background: {config['gradient']}; color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; margin-bottom: 15px; display: flex; align-items: center;">
                <span style="margin-right: 10px;">{icon}</span>{config['title']}
            </h3>
            <div style="line-height: 1.6;">{content}</div>
        </div>
        """
    elif section_type == "instructions":
        return f"""
        <div style="background: {config['gradient']}; color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px;">
            <h3 style="margin-top: 0; margin-bottom: 20px; display: flex; align-items: center;">
                <span style="margin-right: 10px;">{icon}</span>{config['title']}
            </h3>
            <div style="line-height: 1.8; font-size: 16px;">{content}</div>
        </div>
        """
    elif section_type == "tips":
        return f"""
        <div style="background: {config['gradient']}; color: #333; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px;">
            <h3 style="margin-top: 0; margin-bottom: 15px; display: flex; align-items: center;">
                <span style="margin-right: 10px;">{icon}</span>{config['title']}
            </h3>
            <div style="line-height: 1.6;">{content}</div>
        </div>
        """
    else:
        return f"""
        <div style="background: {config['gradient']}; color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; margin-bottom: 15px; display: flex; align-items: center;">
                <span style="margin-right: 10px;">{icon}</span>{config['title']}
            </h3>
            <div style="line-height: 1.6;">{content}</div>
        </div>
        """

def time_template(prep_time, cook_time):
    return f"""
    <strong>Prep:</strong> {prep_time}<br>
    <strong>Cook:</strong> {cook_time}
    """

def serving_template(serving_size, calories):
    return f"""
    <strong>Serves:</strong> {serving_size}<br>
    <strong>Calories:</strong> {calories}
    """