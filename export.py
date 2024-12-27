import os
from datetime import datetime

from airium import Airium


def export_html(html_body: str, a, html_file):
    a("<!DOCTYPE html>")
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t=html_file)

        with a.body():
            with a.h3(id="id23409231", klass="main_header"):
                a(html_body)
    return a


def write_html(html_body: str) -> None:
    a = Airium()

    timestamp = datetime.now().strftime("%m-%d-%y_%H-%M-%I")  # Use safe format
    outfolder = r"/exports/"
    html_filename = f"gemini-export-{timestamp}"
    html_ext = ".html"

    cur_dir = os.getcwd()
    current_wd = cur_dir + outfolder

    html_file = current_wd + html_filename + html_ext

    i = 0

    try:
        if not os.path.exists(current_wd):
            os.makedirs(current_wd)

        a = export_html(html_body, a, html_file)

        if os.path.exists(html_file):
            i += 1
            html_filename + (f"_{i}")
        else:
            with open(html_file, "x") as f:
                f.write(str(a))
    except Exception:
        raise
