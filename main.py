import google.generativeai as genai
from rich.console import Console
from rich.theme import Theme

theme_config = {
    "background": "#1e1e1e",
    "accent1": "#FFD700",
    "accent2": "#A0522D",
    "primary": "#FFFFFF",
    "secondary": "#C0C0C0",
    "error": "#FF0000",
    "warning": "#FFA500",
    "log": {
        "level": {
            "debug": "dim #555555",
            "info": "#FFFFFF",
            "success": "#00FF00",
            "warning": "#FFA500",
            "error": "#FF0000",
            "critical": "#FF0000 bold",
        }
    },
    "progress": {
        "bar": {
            "finished": "#FFD700",
            "percentage": "#FFFFFF",
            "pulse": "#FFFFFF",
        }
    },
}
custom_theme = Theme(
    {
        "debug": theme_config["log"]["level"]["debug"],
        "info": theme_config["log"]["level"]["info"],
        "success": theme_config["log"]["level"]["success"],
        "warning": theme_config["log"]["level"]["warning"],
        "error": theme_config["log"]["level"]["error"],
        "critical": theme_config["log"]["level"]["critical"],
    }
)

if __name__ == "__main__":
    record = False

    console = Console(theme=custom_theme, highlight=True, record=record)

    while True:
        prompt = console.input("> USER: ")

        genai.configure(api_key="AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(str(prompt))

        console.print(f"\n> BOT: {response.text}")

        if record:
            # text output
            print("\nRecorded HTML output:\n", console.export_html())  # HTML output
