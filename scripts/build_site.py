#!/usr/bin/env python3
"""Build script: собирает dist/ru/ и dist/en/ из JSON + Jinja2-шаблона."""

import argparse
import json
import shutil
import sys
import time
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

REQUIRED_FIELDS = {
    "id", "sign_a", "sign_b", "title",
    "description", "compatibility_points", "cliffhanger",
}
EXPECTED_COUNT = 144

# ── Конфиг языков ─────────────────────────────────────────────────────

LANG_CONFIG: dict[str, dict] = {
    "ru": {
        "data": Path("data/compatibility_ru.json"),
        "locale": "ru_RU",
        "ui": {
            "eyebrow":          "Астрологический разбор",
            "h1_prefix":        "Совместимость",
            "h1_and":           "и",
            "subtitle":         "Натальный разбор от Synastry AI",
            "preloader_aria":   "Загрузка анализа",
            "results_aria":     "Результаты совместимости",
            "points_aria":      "Ключевые факты совместимости",
            "point_label":      "Пункт",
            "cliffhanger_aria": "Продолжение анализа",
            "paywall_aria":     "Полный разбор доступен в боте",
            "paywall_p1": (
                "Полный астрологический разбор включает анализ синастрии, аспектов "
                "Венеры и Марса, кармических связей и прогноз на ближайший год. "
                "Также включён персональный календарь благоприятных и опасных периодов."
            ),
            "paywall_p2": (
                "Дополнительно: разбор сексуальной совместимости по натальной карте, "
                "рекомендации по преодолению кризисов и индивидуальные ритуалы."
            ),
            "cta_hint":   "Полный разбор — только в боте",
            "cta_button": "Открыть полный разбор в боте",
            "cta_aria":   "Открыть полный астрологический разбор в Telegram-боте",
            "preloader_phrases": [
                "Анализируем натальные карты...",
                "Сверяем положения Венеры и Марса...",
                "Рассчитываем синастрию...",
                "Изучаем кармические узлы...",
                "Проверяем аспекты Луны...",
                "Сопоставляем стихии и качества...",
                "Формируем итоговый отчёт...",
            ],
            "index_title":    "Все совместимости — Synastry AI",
            "index_h1":       "Все пары <span class=\"accent\">совместимости</span>",
            "index_subtitle": "144 натальных разбора от Synastry AI",
            "index_pair":     "{a} и {b}",
        },
    },
    "en": {
        "data": Path("data/compatibility_en.json"),
        "locale": "en_US",
        "ui": {
            "eyebrow":          "Astrological Reading",
            "h1_prefix":        "Compatibility of",
            "h1_and":           "&",
            "subtitle":         "Natal Analysis by Synastry AI",
            "preloader_aria":   "Loading your analysis",
            "results_aria":     "Compatibility results",
            "points_aria":      "Key compatibility insights",
            "point_label":      "Point",
            "cliffhanger_aria": "There's more to the story",
            "paywall_aria":     "Full reading available in the bot",
            "paywall_p1": (
                "The full astrological reading includes synastry analysis, Venus and Mars "
                "aspects, karmic connections, and a 12-month relationship forecast. "
                "Also included: a personalized calendar of favorable and challenging periods."
            ),
            "paywall_p2": (
                "Additionally: sexual compatibility by natal chart, strategies for navigating "
                "relationship crises, and personalized rituals for strengthening your bond."
            ),
            "cta_hint":   "Full reading — inside the bot",
            "cta_button": "Open full reading in the bot",
            "cta_aria":   "Open the full astrological reading in the Telegram bot",
            "preloader_phrases": [
                "Analyzing natal charts...",
                "Mapping Venus and Mars positions...",
                "Calculating synastry...",
                "Reading karmic nodes...",
                "Checking lunar aspects...",
                "Comparing elements and modalities...",
                "Generating your report...",
            ],
            "index_title":    "All Compatibility Readings — Synastry AI",
            "index_h1":       "All <span class=\"accent\">Compatibility</span> Pairs",
            "index_subtitle": "144 natal readings by Synastry AI",
            "index_pair":     "{a} & {b}",
        },
    },
}

# ── CLI ───────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build multilingual static SEO pages.")
    p.add_argument("--template", type=Path, default=Path("templates/page.html"))
    p.add_argument("--assets",   type=Path, default=Path("assets"))
    p.add_argument("--out",      type=Path, default=Path("dist"))
    p.add_argument("--langs",    nargs="+", default=["ru", "en"],
                   help="Languages to build (default: ru en)")
    p.add_argument("--clean",  action="store_true")
    p.add_argument("--strict", action="store_true")
    return p.parse_args()

# ── Валидация JSON ────────────────────────────────────────────────────

def load_and_validate(data_path: Path) -> list[dict]:
    if not data_path.exists():
        sys.exit(f"[ERROR] Data file not found: {data_path}")
    with data_path.open(encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"[ERROR] Invalid JSON in {data_path}: {e}")
    if not isinstance(data, list):
        sys.exit(f"[ERROR] {data_path}: root must be a list")
    if len(data) != EXPECTED_COUNT:
        print(f"[WARN] {data_path.name}: expected {EXPECTED_COUNT}, got {len(data)}")
    seen: set[str] = set()
    for i, entry in enumerate(data):
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            sys.exit(f"[ERROR] Entry #{i} missing: {missing}")
        if entry["id"] in seen:
            sys.exit(f"[ERROR] Duplicate id: {entry['id']}")
        seen.add(entry["id"])
        if len(entry.get("compatibility_points", [])) != 3:
            sys.exit(f"[ERROR] {entry['id']}: must have exactly 3 points")
    return data

# ── Redirect index ────────────────────────────────────────────────────

def build_redirect_index(out: Path) -> None:
    html = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Synastry AI — Compatibility Readings</title>
  <style>
    body { margin: 0; min-height: 100dvh; display: flex; align-items: center;
           justify-content: center; background: #0A0612; font-family: monospace; }
    a { color: #C49AFF; text-decoration: none; margin: 0 16px; font-size: 16px; }
    a:hover { text-decoration: underline; }
  </style>
  <script>
    (function () {
      var lang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
      window.location.replace(lang.startsWith('ru') ? '/ru/' : '/en/');
    })();
  </script>
</head>
<body>
  <noscript>
    <a href="/ru/">Русская версия</a>
    <a href="/en/">English version</a>
  </noscript>
</body>
</html>
"""
    (out / "index.html").write_text(html, encoding="utf-8")
    print("[OK] dist/index.html (language redirect)")

# ── Lang index ────────────────────────────────────────────────────────

def build_lang_index(data: list[dict], out: Path, lang: str, ui: dict) -> None:
    pair_tmpl = ui["index_pair"]
    items = "\n".join(
        f'  <li><a href="compatibility/{e["id"]}.html">'
        f'{pair_tmpl.format(a=e["sign_a"]["name"], b=e["sign_b"]["name"])}</a></li>'
        for e in data
    )
    css_path = "/assets/style.css"
    html = (
        f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n'
        f'  <meta charset="UTF-8">\n'
        f'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'  <title>{ui["index_title"]}</title>\n'
        f'  <link rel="stylesheet" href="{css_path}">\n'
        f'</head>\n<body>\n'
        f'  <div class="bg-blob bg-blob--1"></div>\n'
        f'  <div class="bg-blob bg-blob--2"></div>\n'
        f'  <main class="container">\n'
        f'    <header class="hero">\n'
        f'      <h1 class="hero__title">{ui["index_h1"]}</h1>\n'
        f'      <p class="hero__subtitle">{ui["index_subtitle"]}</p>\n'
        f'    </header>\n'
        f'    <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">\n'
        f'{items}\n    </ul>\n'
        f'  </main>\n</body>\n</html>\n'
    )
    (out / "index.html").write_text(html, encoding="utf-8")

# ── Размер дерева ─────────────────────────────────────────────────────

def tree_size_kb(root: Path) -> float:
    return sum(f.stat().st_size for f in root.rglob("*") if f.is_file()) / 1024

# ── Sitemap ───────────────────────────────────────────────────────────

DOMAIN = "https://synastry.space"
SITEMAP_LANGS = ("ru", "en")

def build_sitemap(out: Path) -> None:
    lastmod = date.today().isoformat()
    urls: list[str] = []

    for lang in SITEMAP_LANGS:
        lang_dir = out / lang
        if not lang_dir.exists():
            continue
        for html_file in sorted(lang_dir.rglob("*.html")):
            rel = html_file.relative_to(out).as_posix()
            # index.html → чистый путь без файла
            if rel.endswith("/index.html"):
                url_path = rel[: -len("index.html")]
            else:
                url_path = rel
            urls.append(
                f"  <url>\n"
                f"    <loc>{DOMAIN}/{url_path}</loc>\n"
                f"    <lastmod>{lastmod}</lastmod>\n"
                f"  </url>"
            )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )

    sitemap_path = out / "sitemap.xml"
    sitemap_path.write_text(xml, encoding="utf-8")
    print(f"[OK] sitemap.xml: {len(urls)} URLs -> {sitemap_path}")


# ── Основная сборка ───────────────────────────────────────────────────

def build(args: argparse.Namespace) -> None:
    start = time.perf_counter()

    if not args.template.exists():
        sys.exit(f"[ERROR] Template not found: {args.template}")

    # Очистка
    if args.clean and args.out.exists():
        shutil.rmtree(args.out)
        print(f"[OK] Cleaned: {args.out}")

    args.out.mkdir(parents=True, exist_ok=True)

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(str(args.template.parent)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(args.template.name)

    # Shared assets (один раз)
    if args.assets.exists():
        shutil.copytree(args.assets, args.out / "assets", dirs_exist_ok=True)
        print(f"[OK] Assets -> dist/assets/")
    else:
        print(f"[WARN] Assets dir not found: {args.assets}")

    # Redirect index
    build_redirect_index(args.out)

    total_built = 0
    total_errors = 0

    for lang in args.langs:
        if lang not in LANG_CONFIG:
            print(f"[WARN] Unknown lang '{lang}', skipping")
            continue

        cfg = LANG_CONFIG[lang]
        data = load_and_validate(cfg["data"])
        ui = cfg["ui"]
        locale = cfg["locale"]

        lang_dir = args.out / lang
        pages_dir = lang_dir / "compatibility"
        pages_dir.mkdir(parents=True, exist_ok=True)

        success = errors = 0

        for entry in data:
            try:
                rendered = template.render(
                    **entry,
                    lang=lang,
                    locale=locale,
                    ui=ui,
                )
                out_file = pages_dir / f'{entry["id"]}.html'
                out_file.write_text(rendered, encoding="utf-8")
                success += 1
            except Exception as e:
                print(f'[ERROR] [{lang}] pair={entry.get("id","?")} — {e}')
                errors += 1
                if args.strict:
                    sys.exit(1)

        build_lang_index(data, lang_dir, lang, ui)

        print(f"[OK] [{lang.upper()}] {success}/{len(data)} pages -> dist/{lang}/")
        total_built += success
        total_errors += errors

    build_sitemap(args.out)

    elapsed = time.perf_counter() - start
    size_kb = tree_size_kb(args.out)

    print()
    print(f"[OK] Built:  {total_built} pages total")
    if total_errors:
        print(f"[WARN] Errors: {total_errors}")
    print(f"[OK] Time:   {elapsed:.2f}s")
    print(f"[OK] Size:   {size_kb:.1f} KB")
    print(f"[OK] Output: {args.out.resolve()}")


if __name__ == "__main__":
    build(parse_args())
