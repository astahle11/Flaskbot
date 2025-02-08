import time

import google.api_core.exceptions
import google.generativeai as genai
from google.generativeai import GenerationConfig

import export


def main(gemini_config, console):
    export_html = False 
    try:
        console = console

        version_num = gemini_config["version_num"]
        print(version_num)

        api_key = gemini_config["api_key"]
        model_name = gemini_config["model_name"]

        while True:
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
                    temperature=0.3,  # Controls ranccdomness, higher values = more random
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
                if quit_prompt.strip() != "y" or "n":
                    raise KeyboardInterrupt

            except google.api_core.exceptions.TooManyRequests as e:
                console.print(f"{e}", style="error")
                console.print(
                    "Too many requests. 1 minute wait period until next query.\n",
                    style="error",
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
            export.write_html(html_body)
            console.print("Done.", style="system")
            exit()


if __name__ == "__main__":
    main()
