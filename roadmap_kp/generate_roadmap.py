#!/usr/bin/env python3
"""
Генератор дорожной карты и сметы проекта - Global Generation.

Отдельное PDF-приложение к основному workplan для клиентов, которым нужна
операционная детализация: таймлайн по датам, смета расходов, риски.

Использование:
    python generate_roadmap.py input.json
    python generate_roadmap.py input.json --output custom_name.pdf

Входной JSON может быть общим с workplan (оба генератора читают свои поля).
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


def validate_data(data: dict) -> list[str]:
    """Проверяет наличие обязательных полей для roadmap."""
    required = [
        "client_name",
        "timeline", "cost_preparation", "cost_mentorship",
        "cost_tuition", "totals",
    ]
    missing = [f for f in required if f not in data]
    return missing


def render_pdf(data: dict, output_path: Path) -> Path:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("roadmap.html")

    if "date" not in data:
        data["date"] = datetime.now().strftime("%d.%m.%Y")

    html_string = template.render(**data)
    html = HTML(string=html_string, base_url=str(TEMPLATES_DIR))
    html.write_pdf(str(output_path))

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Использование: python generate_roadmap.py input.json [--output name.pdf]")
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

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_name = sys.argv[idx + 1]
    else:
        safe_name = data["client_name"].replace(" ", "_")
        output_name = f"roadmap_{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / output_name

    print(f"Генерация roadmap PDF для: {data['client_name']}")
    result = render_pdf(data, output_path)
    print(f"PDF сохранён: {result}")


if __name__ == "__main__":
    main()
