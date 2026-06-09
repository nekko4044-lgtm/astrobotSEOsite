#!/usr/bin/env python3
"""Inject ZodiacWidget calculator into all compatibility pages in dist/."""

from pathlib import Path

DIST = Path(__file__).parent.parent / "dist"

CALC_BLOCK = """
        <!-- ── Zodiac Calculator ── -->
        <section class="calc-widget glass-card" aria-label="Sign compatibility calculator">
          <p class="calc-widget__title" id="calcTitle"></p>
          <div class="calc-widget__row">
            <select class="calc-widget__select" id="calcSign1" aria-label="Sign 1"></select>
            <span class="calc-widget__sep" aria-hidden="true">♥</span>
            <select class="calc-widget__select" id="calcSign2" aria-label="Sign 2"></select>
            <button class="calc-widget__btn" onclick="calcGo()"></button>
          </div>
        </section>
        <script>
        (function(){
          var EN=['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces'];
          var LABELS={
            ru:['Овен','Телец','Близнецы','Рак','Лев','Дева','Весы','Скорпион','Стрелец','Козерог','Водолей','Рыбы'],
            en:['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
          };
          var UI={
            ru:{title:'Выбери другую пару',btn:'Рассчитать'},
            en:{title:'Try another pair',btn:'Calculate'}
          };
          var path=window.location.pathname;
          var lang=path.startsWith('/ru')?'ru':'en';
          var m=path.match(/\\/([a-z]+-[a-z]+)\\.html/);
          var pair=m?m[1].split('-'):['aries','aries'];
          var s1=pair[0],s2=pair[1];
          document.getElementById('calcTitle').textContent=UI[lang].title;
          document.querySelector('.calc-widget__btn').textContent=UI[lang].btn;
          [['calcSign1',s1],['calcSign2',s2]].forEach(function(p){
            var sel=document.getElementById(p[0]);
            EN.forEach(function(slug,i){
              var o=document.createElement('option');
              o.value=slug;o.textContent=LABELS[lang][i];
              if(slug===p[1])o.selected=true;
              sel.appendChild(o);
            });
          });
          window.calcGo=function(){
            var v1=document.getElementById('calcSign1').value;
            var v2=document.getElementById('calcSign2').value;
            window.location.href='/'+lang+'/compatibility/'+v1+'-'+v2;
          };
        })();
        </script>

"""

INJECT_AFTER = "        </header>"
MARKER = "calc-widget"


def inject_all():
    ru_pages = list((DIST / "ru" / "compatibility").glob("*.html"))
    en_pages = list((DIST / "en" / "compatibility").glob("*.html"))
    pages = ru_pages + en_pages

    updated = skipped = errors = 0

    for f in pages:
        html = f.read_text(encoding="utf-8")

        if MARKER in html:
            skipped += 1
            continue

        if INJECT_AFTER not in html:
            print(f"[WARN] No injection point in {f.name}")
            errors += 1
            continue

        new_html = html.replace(INJECT_AFTER, INJECT_AFTER + CALC_BLOCK, 1)
        f.write_text(new_html, encoding="utf-8")
        updated += 1

    print(f"Done — updated: {updated}, skipped: {skipped}, errors: {errors}")


if __name__ == "__main__":
    inject_all()
