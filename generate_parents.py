#!/usr/bin/env python3
"""
Генератор PDF-документа для родителей Global Generation.

Использование:
    python generate_parents.py
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("parents.html")
    html_string = template.render()

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "GG_Для_родителей.pdf"

    print("Генерация PDF для родителей...")
    html = HTML(string=html_string, base_url=str(TEMPLATES_DIR))
    html.write_pdf(str(output_path))
    print(f"PDF сохранён: {output_path}")


if __name__ == "__main__":
    main()
