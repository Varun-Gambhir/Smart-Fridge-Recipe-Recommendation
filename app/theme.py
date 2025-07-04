from gradio.themes.base import Base

class CoolTheme(Base):
    def style(self):
        return super().style(
            button_primary_background="linear-gradient(90deg, #4facfe 0%, #00f2fe 100%)",
            button_primary_text_color="white",
            button_primary_border_radius="12px",
            block_background_fill="linear-gradient(to right, #ffffff, #f8faff)",
            block_border_width="0px",
            block_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
            container_radius="18px"
        )