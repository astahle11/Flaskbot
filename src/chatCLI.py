#!/usr/bin/env python

import sys
import time

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from rich.console import Console
from rich.theme import Theme


import models.gemini

run_gemini = True
run_deepseekV3 = False

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

gemini_config = {
    "version_num": "0.1.0-alpha.4",
    "api_key": "AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw",
    "model_name": "gemini-1.5-pro-latest",
}


class Common:
    """This is a class for reusing code like exit messages, errors, etc."""

    @staticmethod
    def intro(version_num, model_name) -> None:
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
        "background": "#1C1C1C",
        "chatbot": "dark_slate_gray2",
        "user": "bold grey70",
        "system": "bold bright_white",
        "info": "cyan2",
        "error": "#FF4500",
        "highlight": "#32CD32",
    },
    inherit=False,
)


console = Console(color_system="auto", soft_wrap=True, record=True, theme=custom_theme)


def main():
    # Initialize as false in case the program exits before any response content is generated.

    """app = QApplication(sys.argv)
    w = QMainWindow()
    w.show()
    app.exec()
    """

    if run_gemini is True:
        Common.intro(gemini_config["version_num"], gemini_config["model_name"])
        models.gemini.main(gemini_config, console)


if __name__ == "__main__":
    main()
