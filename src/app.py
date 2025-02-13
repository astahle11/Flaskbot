#!/usr/bin/env python

import sys
from flask import Flask, render_template
from flask_socketio import SocketIO, send
import values
import google.api_core.exceptions
import google.generativeai as genai
from google.generativeai import GenerationConfig
import webbrowser
from threading import Timer
import time
from datetime import datetime
import logging


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


app = Flask(__name__)
app.logger.setLevel(logging.WARNING)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return render_template("index.html")


class Models:
    def __init__(self, **kwargs):
        self.message = kwargs

    def _ai_gemini(self):
        api_key = values.gemini_config["api_key"]
        model_name = values.gemini_config["model_name"]

        config = GenerationConfig(
            max_output_tokens=2000,  # Maximum number of tokens in the response
            temperature=0.3,  # Controls ranccdomness, higher values = more random
            top_k=40,  # Number of top tokens to consider for sampling
            top_p=0.95,  # Cumulative probability threshold for sampling
        )

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(str(self.message), generation_config=config)
        bot_response = response.text.strip()  # Ensure clean output
        return bot_response

    def _ai_deepseek(self):
        api_key = values.open_router_key
        pass  # tbd


@socketio.on("message")
def handle_message(message, models: Models):
    send(f"{message}")
    logging.info(message)

    if values.select_Gemini is True:
        bot_response = models.ai_gemini(message)
    if values.select_Deepseek is True:
        bot_response = models.ai_deepseek(message)

    send(bot_response)
    logging.info(bot_response)


def open_browser():
    webbrowser.open("http://localhost:5000")


def main():
    Models()
    try:
        socketio.run(app, host="0.0.0.0", port=5000, debug=False, log_output=False)

        Timer(1, open_browser).start()  # Wait 1 second before opening
        app.run(debug=False)

    except google.api_core.exceptions.TooManyRequests as e:
        send(f"{e}")
        send(
            "Too many requests. 1 minute wait period until next query.\n",
            style="error",
        )
        time.sleep(60)

    except Exception as e:
        send(f"Exception occurred: {e}", style="error")

    except KeyboardInterrupt:
        pass

    except (
        google.api_core.exceptions.InternalServerError,
        google.api_core.exceptions.GatewayTimeout,
        google.api_core.exceptions.ServerError,
        google.api_core.exceptions.ServiceUnavailable,
        google.api_core.exceptions.Unknown,
    ) as e:
        send(f"API error occurred: {e}", style="error")
        send("Resuming...")
        time.sleep(2)


if __name__ == "__main__":
    main()
