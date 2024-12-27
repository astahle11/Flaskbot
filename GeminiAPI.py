from datetime import datetime

import google.generativeai as genai
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

theme = Theme(
    {
        "background": "black",  # Dark background for contrast
        "chatbot": "chartreuse1",  # Light cyan for the chatbot
        "user": "cyan1",  # Bright green for the user
        "system": "bright_white",  # Bright yellow for system messages
        "info": "bright_blue",  # Bright blue for informational messages
        "error": "bright_red",  # Bright red for error messages
        "highlight": "bright_magenta",  # Bright magenta for highlighted text
    }
)


def export_html(response):
    with open("output.html", "w") as f:
        f.write(response(datetime.now))
    return


if __name__ == "__main__":
    try:
        console = Console(
            color_system="auto", soft_wrap=True, record=False, theme=theme
        )

        console.print(
            Text(
                "Welcome to AI Chat. Type 'exit' to quit.\n",
                style="system",
            )
        )

        while True:
            console.print("[You]: ", style="user", end="")
            user_input = input("")

            genai.configure(api_key="AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(str(user_input))

            response = response.text
            console.print("\n[Gemini]:", style="chatbot", end=" ")
            console.print(f"{response}")

            # Exit condition
            if input.lower() == "exit":
                console.print("\nGoodbye!", style="system")
                break

    except Exception as e:
        console.print("Exception:", e, style="error")

    finally:
        if console.record:
            # text output
            print(
                "\nRecorded HTML output:\n", export_html(response), style="system"
            )  # HTML output
