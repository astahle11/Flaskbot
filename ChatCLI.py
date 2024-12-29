#!/usr/bin/env python

import sys
import time

import google.api_core.exceptions
import google.generativeai as genai
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from export import write_html

"""
[GPLv3 LICENSE] 
This program is free software: you can redistribute it and/or` modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

"""
sys.tracebacklimit = 5

version_num = "1.0"

api_key = "AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw"
gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=YOUR_API_KEY"


model_name = "gemini-1.5-flash"

theme = Theme(
    {
        "background": "black",
        "chatbot": "green1",
        "user": "cyan1",
        "system": "bright_white",
        "info": "bright_blue",
        "error": "bright_red",
        "highlight": "bright_magenta",
    }
)


cyberpunk_theme = Theme(
    {
        "background": "#1C1C1C",  # Dark Gray background
        "chatbot": "dark_slate_gray2",  # Bright Magenta (Cyberpunk vibe)
        "user": "bold grey70",  # Neon Cyan
        "system": "bold bright_white",  # Bold Bright White for system messages
        "info": "cyan2",  # Neon Blue for information
        "error": "#FF4500",  # Orange-Red for errors
        "highlight": "#32CD32",  # Bright Lime Green for highlights
    },
    inherit=False,
)

console = Console(
    color_system="auto", soft_wrap=True, record=True, theme=cyberpunk_theme
)


def main():
    """Main code block. Does the following:

    - Initializes the rich console
    - Initializes the "content" variable (where the discussion will be stored)
    - Accepts user input and appends the string to the contents list.
    - Configures the response model and then appends the response to the contents list.
    - Joins the collected content strings and replaces newlines with html breaks.
    - Regardless of how the script is ended, the finally block calls the HTML functions in export.py
      and writes the HTML file.
    - Exports are saved in /exports, which is created in the same directory that the script is in.

    """
    try:
        console.print(
            Text(f"# ChatCLI Version: {version_num} #\n"),
            style="system",
            no_wrap=True,
            justify="left",
        )

        while True:
            content = []

            while True:
                str(console.print("You: ", style="user", end=""))
                user_input = input("")
                if user_input.strip():
                    break
                else:
                    continue

            if user_input == "q":
                exit()

            content.append("\nYou: " + user_input)

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(str(user_input))

            str(console.print("\nBot: ", style="chatbot", end=""))
            console.print(f"{response.text}")

            content.append("AI: " + response.text)

            html_body = "\n".join(content).replace("\n", "<br>")

    except Exception as e:
        console.print(f"Exception occurred: {e}", style="error")

    except (
        google.api_core.exceptions.InternalServerError,
        google.api_core.exceptions.GatewayTimeout,
        google.api_core.exceptions.ServerError,
        google.api_core.exceptions.ServiceUnavailable,
        google.api_core.exceptions.Unknown,
    ) as e:
        console.print(f"API error occurred: {e}", style="error")
        console.print("Resuming...")
        time.sleep(2)

        # Do not return, just continue the execution of the script

    except KeyboardInterrupt:
        pass

    finally:
        console.print("\nRecording HTML output...", style="system")
        write_html(html_body)
        quit()


if __name__ == "__main__":
    main()
