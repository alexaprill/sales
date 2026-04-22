#!/usr/bin/env python3
"""
Генератор персонального плана работы — Global Generation.

Использование:
    python generate_workplan.py input.json
    python generate_workplan.py input.json --output custom_name.pdf

Входной JSON должен содержать все поля для шаблона workplan.html.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


def validate_data(data: dict) -> list[str]:
    """Проверяет наличие обязательных полей."""
    required = [
        "client_name", "greeting_text",
        "strengths", "growth_areas", "work_plan",
        "recommendation", "formats",
        "urgency_text", "special_offer", "cta",
    ]
    missing = [f for f in required if f not in data]
    return missing


def render_pdf(data: dict, output_path: Path) -> Path:
    """Рендерит HTML-шаблон с данными и конвертирует в PDF."""
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("workplan.html")

    # Дата по умолчанию — сегодня
    if "date" not in data:
        data["date"] = datetime.now().strftime("%d.%m.%Y")

    html_string = template.render(**data)

    # WeasyPrint нужен base_url для загрузки ассетов (изображения)
    html = HTML(string=html_string, base_url=str(TEMPLATES_DIR))
    html.write_pdf(str(output_path))

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Использование: python generate_workplan.py input.json [--output name.pdf]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Файл не найден: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    missing = validate_data(data)
    if missing:
        print(f"Отсутствуют обязательные поля: {', '.join(missing)}")
        sys.exit(1)

    # Определяем имя выходного файла
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_name = sys.argv[idx + 1]
    else:
        # Формат: "КП для <Имя>.pdf". Если задан client_name_genitive - используем его
        # (например "Артёма" вместо "Артём") для естественного звучания на русском.
        name_for_file = data.get("client_name_genitive", data["client_name"])
        output_name = f"КП для {name_for_file}.pdf"

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / output_name

    print(f"Генерация PDF для: {data['client_name']}")
    result = render_pdf(data, output_path)
    print(f"PDF сохранён: {result}")


if __name__ == "__main__":
    main()
