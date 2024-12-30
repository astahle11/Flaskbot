#!/usr/bin/env python

import sys
import time

import google.api_core.exceptions
import google.generativeai as genai
from google.generativeai import GenerationConfig
from rich.console import Console
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
sys.tracebacklimit = 0
version_num = "0.1.0-alpha.4"
api_key = "AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw"
model_name = "gemini-1.5-pro-latest"


class Common:
    @staticmethod
    def intro() -> None:
        console.print(
            f"\nChatCLI [Version: {version_num}]",
            style="system",
            no_wrap=True,
            justify="left",
        )
        console.print("Model: ", style="bright_white", end="")
        console.print(f"{model_name}", style="cyan2")
        console.print("CTRL-C to quit.", style="bright_white")

    @staticmethod
    def exitmsg() -> None:
        console.print("(Press Enter to quit)", style="bright_white", end="")
        input()


custom_theme = Theme(
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

console = Console(color_system="auto", soft_wrap=True, record=True, theme=custom_theme)


def main():
    export_html = False  # Initialize as false in case the program exits before any response content is generated.

    try:
        Common.intro()

        while True:
            export_html = export_html
            content: list = []
            try:
                while True:
                    str(console.print("\nYou: ", style="user", end=""))
                    user_input = input("")

                    if user_input.strip():
                        break
                    else:
                        console.print("\n", end="")
                        continue

                content.append("\nYou: " + user_input)

                config = GenerationConfig(
                    max_output_tokens=2000,  # Maximum number of tokens in the response
                    temperature=0.3,  # Controls randomness, higher values = more random
                    top_k=40,  # Number of top tokens to consider for sampling
                    top_p=0.95,  # Cumulative probability threshold for sampling
                )

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    str(user_input), generation_config=config
                )

                str(console.print("\nBot: ", style="chatbot"))
                console.print(f"{response.text}")

                content.append("\nBot: " + response.text)

                html_body = "\n".join(content).replace("\n", "<br>")

                export_html = True  # Once html_body is written to once, exporting an HTML is okay.

            except KeyboardInterrupt:
                console.print("\n", end="")
                console.print("\nQuit? y/n", style="system")
                quit_prompt = input("")

                if quit_prompt.strip() == "y":
                    raise
                if quit_prompt.strip() == "n":
                    continue

            except google.api_core.exceptions.TooManyRequests as e:
                console.print(f"{e}")
                console.print(
                    "Too many requests. 1 minute wait period until next query.\n"
                )
                time.sleep(60)
                continue

    except Exception as e:
        console.print(f"Exception occurred: {e}", style="error")

    except KeyboardInterrupt:
        pass

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

    finally:
        if not export_html:
            exit()

        else:
            console.print("\nRecording HTML output...", style="system")
            write_html(html_body)
            console.print("Done.", style="system")
            exit()


if __name__ == "__main__":
    main()
