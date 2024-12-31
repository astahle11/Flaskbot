#!/usr/bin/env python
import os
from datetime import datetime

from airium import Airium


def export_html(html_body: str, a, path_to_html):
    """Export contents of chat into an HTML format.

    Args:
        html_body (str): String of user input and AI responses from current session.
        a (Airium): Represents the airium object.
        path_to_html (str): Path where html files are saved.

    Returns:
        a: Return the Airium object.
    """
    a("<!DOCTYPE html>")
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t=path_to_html)

        with a.body():
            with a.h3(id="id23409231", klass="main_header"):
                a(html_body)
    return a


def write_html(html_body: str) -> None:
    """Write the html file to the exports folder.
    Args:
        html_body (str): String of user input and AI responses from current session.
    """
    a = Airium()

    timestamp = datetime.now().strftime("%m-%d-%y_%H-%M-%I")  # Use safe format
    outfolder = r"/exports/"
    html_filename = f"gemini-export-{timestamp}"
    html_ext = ".html"

    cur_dir = os.getcwd()
    current_wd = cur_dir + outfolder

    path_to_html = current_wd + html_filename + html_ext

    i = 0

    try:
        if not os.path.exists(current_wd):
            os.makedirs(current_wd)

        a = export_html(html_body, a, path_to_html)

        if os.path.exists(path_to_html):
            i += 1
            html_filename + (f"_{i}")
        else:
            with open(path_to_html, "x") as f:
                f.write(str(a))
    except Exception:
        raise
