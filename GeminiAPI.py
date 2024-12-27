import google.generativeai as genai
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from export import write_html

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


def main():
    try:
        console = Console(color_system="auto", soft_wrap=True, record=True, theme=theme)
        console.print(
            Text(
                "Welcome to AI Chat. Press CTRL-C to quit.\n",
                style="system",
            )
        )

        while True:
            content = []
            str(console.print("You: ", style="user", end=""))
            user_input = input("")

            content.append("\nYou: " + user_input)

            genai.configure(api_key="AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(str(user_input))

            str(console.print("\nGemini: ", style="chatbot", end=""))
            console.print(f"{response.text}")

            content.append("\nGemini: " + response.text)

            html_body = "\n".join(content).replace("\n", "<br>")

    # Exit condition
    except KeyboardInterrupt:
        pass

    except Exception as e:
        console.print("EXCEPTION: \n", e, style="error")

    finally:
        console.print("\n\nRecording HTML output...", style="system")
        write_html(html_body)

        console.print("Exiting!", style="system")
        quit()


if __name__ == "__main__":
    main()
