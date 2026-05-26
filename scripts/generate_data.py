#!/usr/bin/env python3
"""Генерирует data/compatibility_ru.json и data/compatibility_en.json — 144 пары."""

import itertools
import json
import random
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════
# ЗНАКИ / SIGNS
# ═══════════════════════════════════════════════════════════════════════

SIGNS_RU = [
    {"slug": "aries",       "name": "Овен",       "name_gen": "Овна",     "element": "огонь", "quality": "кардинальный"},
    {"slug": "taurus",      "name": "Телец",      "name_gen": "Тельца",   "element": "земля", "quality": "фиксированный"},
    {"slug": "gemini",      "name": "Близнецы",   "name_gen": "Близнецов","element": "воздух","quality": "мутабельный"},
    {"slug": "cancer",      "name": "Рак",        "name_gen": "Рака",     "element": "вода",  "quality": "кардинальный"},
    {"slug": "leo",         "name": "Лев",        "name_gen": "Льва",     "element": "огонь", "quality": "фиксированный"},
    {"slug": "virgo",       "name": "Дева",       "name_gen": "Девы",     "element": "земля", "quality": "мутабельный"},
    {"slug": "libra",       "name": "Весы",       "name_gen": "Весов",    "element": "воздух","quality": "кардинальный"},
    {"slug": "scorpio",     "name": "Скорпион",   "name_gen": "Скорпиона","element": "вода",  "quality": "фиксированный"},
    {"slug": "sagittarius", "name": "Стрелец",    "name_gen": "Стрельца", "element": "огонь", "quality": "мутабельный"},
    {"slug": "capricorn",   "name": "Козерог",    "name_gen": "Козерога", "element": "земля", "quality": "кардинальный"},
    {"slug": "aquarius",    "name": "Водолей",    "name_gen": "Водолея",  "element": "воздух","quality": "фиксированный"},
    {"slug": "pisces",      "name": "Рыбы",       "name_gen": "Рыб",      "element": "вода",  "quality": "мутабельный"},
]

SIGNS_EN = [
    {"slug": "aries",       "name": "Aries",       "element": "fire",  "quality": "cardinal"},
    {"slug": "taurus",      "name": "Taurus",      "element": "earth", "quality": "fixed"},
    {"slug": "gemini",      "name": "Gemini",      "element": "air",   "quality": "mutable"},
    {"slug": "cancer",      "name": "Cancer",      "element": "water", "quality": "cardinal"},
    {"slug": "leo",         "name": "Leo",         "element": "fire",  "quality": "fixed"},
    {"slug": "virgo",       "name": "Virgo",       "element": "earth", "quality": "mutable"},
    {"slug": "libra",       "name": "Libra",       "element": "air",   "quality": "cardinal"},
    {"slug": "scorpio",     "name": "Scorpio",     "element": "water", "quality": "fixed"},
    {"slug": "sagittarius", "name": "Sagittarius", "element": "fire",  "quality": "mutable"},
    {"slug": "capricorn",   "name": "Capricorn",   "element": "earth", "quality": "cardinal"},
    {"slug": "aquarius",    "name": "Aquarius",    "element": "air",   "quality": "fixed"},
    {"slug": "pisces",      "name": "Pisces",      "element": "water", "quality": "mutable"},
]

# ═══════════════════════════════════════════════════════════════════════
# RUSSIAN CONTENT
# ═══════════════════════════════════════════════════════════════════════

RU_ELEMENT_POINTS: dict[str, list[str]] = {
    "огонь+огонь": [
        "{A} и {B} создают союз двух горящих сердец — между ними никогда не бывает скучно, но пламя может сжечь само себя, если оба тянут одеяло на себя.",
        "Два огня в одном пространстве — это бесконечная конкуренция за лидерство. {A} и {B} восхищаются друг другом, но уступать не умеет ни один.",
        "Страсть здесь зашкаливает с первых часов знакомства: {A} узнаёт в {B} себя — и это одновременно восхищает и раздражает.",
        "Ссоры {A} и {B} громкие и яростные, но примирения — столь же горячие. Этот союз никогда не существует в полутонах.",
        "Энергия этой пары заражает всех вокруг — они способны сдвинуть горы, если направят огонь в одну сторону, а не друг на друга.",
        "Главная ловушка {A} и {B} — оба слишком импульсивны, чтобы вовремя остановиться в споре. Побеждает тот, кто первым научится молчать.",
        "В постели между {A} и {B} горит такой жар, что соседи завидуют. Сексуальная химия — безусловный козырь этого союза.",
        "Финансовые амбиции у обоих огромные, но расходы — тоже. {A} и {B} либо строят империю вместе, либо разоряются с улыбкой.",
    ],
    "огонь+земля": [
        "Огненная страсть {A} сталкивается с земным упрямством {B} — это создаёт мощное физическое притяжение в первые месяцы.",
        "{B} даёт {A} ту стабильность, которой ему критически не хватает, но взамен требует терпения, которым {A} не обладает от природы.",
        "Финансовые вопросы — главная точка напряжения: {A} тратит импульсивно, {B} копит методично.",
        "{A} вдохновляет {B} рисковать и выходить за привычные границы, а {B} не даёт {A} поджечь всё вокруг ради красивого жеста.",
        "В долгосрочной перспективе {B} может начать задыхаться от темпа, который задаёт {A}. Компромисс возможен, но даётся нелегко.",
        "Физически эта пара часто гармонична: земля принимает огонь и даёт ему форму, не позволяя разгуляться бесконтрольно.",
        "{A} воспринимает осторожность {B} как занудство, {B} видит в порывах {A} безответственность — и оба отчасти правы.",
        "Когда они находят общий язык, получается нечто выдающееся: энергия {A} плюс надёжность {B} = пара, которая реально строит будущее.",
    ],
    "огонь+воздух": [
        "{A} и {B} — пара, которая не знает тишины: разговоры, планы, споры, смех. Скука в этом союзе физически невозможна.",
        "Воздух раздувает огонь — {B} умеет восхищаться {A} так, что тот начинает гореть ещё ярче.",
        "Интеллектуальная совместимость здесь высокая, но {A} хочет действовать прямо сейчас, а {B} ещё анализирует варианты.",
        "Романтика между {A} и {B} лёгкая и воздушная — никакой тяжёлой привязанности, зато много свободы и доверия.",
        "{B} иногда кажется {A} слишком холодным, а {A} кажется {B} слишком требовательным эмоционально.",
        "Совместные путешествия, авантюры и эксперименты — главный клей этого союза. Рутина убивает их быстрее всего.",
        "В спорах {B} апеллирует к логике, {A} — к чувствам. Со временем они учатся переключаться между этими языками.",
        "Эта пара часто выглядит со стороны идеально — яркая, активная, интересная. Но внутри бывает больше хаоса, чем кажется.",
    ],
    "огонь+вода": [
        "{A} и {B} — классическое противоречие: огонь хочет гореть, вода хочет глубины. Притяжение есть, но взаимопонимание даётся потом.",
        "Эмоциональная глубина {B} пугает и одновременно завораживает {A}. {A} никогда раньше не чувствовал себя настолько понятым — и настолько уязвимым.",
        "Главный конфликт: {A} реагирует на мир действием, {B} — чувством. Один и тот же кризис они переживают совершенно по-разному.",
        "{B} умеет чувствовать {A} без слов — это одновременно дар и угроза для {A}, привыкшего контролировать уязвимость.",
        "Сексуальная совместимость здесь взрывная: интуиция {B} идеально дополняет страсть {A}.",
        "Когда {A} злится, {B} замыкается — и тишина становится страшнее любого скандала.",
        "{B} нуждается в эмоциональной безопасности, которую {A} не всегда умеет давать.",
        "Если {A} научится замедляться, а {B} — открываться, этот союз превратится в нечто редкое: глубину плюс яркость.",
    ],
    "земля+земля": [
        "{A} и {B} строят отношения как хороший дом: медленно, надёжно и на века.",
        "Финансовая совместимость у этой пары — одна из лучших в зодиаке. Оба умеют зарабатывать и сохранять.",
        "Проблема {A} и {B} — слишком много стабильности. Если не вносить что-то новое намеренно, рутина поглощает страсть.",
        "Телесная близость для этой пары — не просто удовольствие, а язык любви. Физический контакт им нужен ежедневно.",
        "Оба упрямы, оба правы, оба не умеют первыми извиняться. Кризисы у них затяжные — но выходят из них тоже вместе.",
        "{A} и {B} создают ощущение вечности: рядом с этим человеком не страшно ничего — ни кризис, ни болезнь.",
        "Консерватизм обоих иногда мешает росту: они могут годами обсуждать перемены, так и не решившись.",
        "Их отношения часто выглядят «скучными» снаружи — но внутри это тихое, глубокое счастье.",
    ],
    "земля+воздух": [
        "{A} ищет стабильности, {B} ищет свободы. Между ними постоянный негласный договор: ты не давишь, я не исчезаю.",
        "Интеллект {B} восхищает практичного {A}. Идеи воздуха обретают форму благодаря земле.",
        "{B} воспринимает структурированность {A} как клетку, {A} воспринимает непостоянство {B} как ненадёжность.",
        "В бытовых вопросах — полная противоположность: {A} хочет порядка, {B} живёт в творческом хаосе.",
        "Разговоры у {A} и {B} могут длиться часами: {B} генерирует идеи, {A} отвечает «как это реализовать».",
        "Социально они дополняют друг друга: {B} открывает новые круги, {A} даёт ощущение дома и якоря.",
        "Эмоциональная дистанция {B} иногда ранит {A}, привыкшего к конкретным проявлениям любви.",
        "Совместные проекты часто успешны: голова {B} плюс руки {A} — реальный результат.",
    ],
    "земля+вода": [
        "{A} и {B} — союз, где каждый чувствует себя понятым. Земля не боится глубины воды.",
        "{B} умеет размягчать {A} — там, где земля была жёсткой, вода находит трещины и проникает внутрь.",
        "Финансово эта пара очень устойчива: практичность {A} и интуиция {B} дают редкие по качеству решения.",
        "Главный риск — созависимость. {B} может стать слишком нужным, а {A} — слишком удобным.",
        "В кризисах {A} стабилизирует {B}: когда эмоции захлёстывают, рядом всегда есть берег.",
        "Физическая близость здесь глубокая и чувственная — терпение {A} и интуиция {B}.",
        "{A} иногда кажется {B} слишком холодным — хотя за этим скрывается просто другой способ любить.",
        "Это один из самых устойчивых союзов зодиака — не яркий, но настоящий.",
    ],
    "воздух+воздух": [
        "{A} и {B} — пара, которая никогда не замолкает. Их связь начинается в голове и только потом спускается в сердце.",
        "Интеллектуальная совместимость здесь максимальная — понимают шутки с полуслова.",
        "Оба избегают тяжёлых эмоций и решают проблемы рационально. Это удобно, пока кому-то не нужно просто выплакаться.",
        "Свобода — главная ценность обоих. Умеют давать друг другу пространство без чувства угрозы.",
        "Физически между {A} и {B} иногда не хватает тепла — слишком много в голове, слишком мало в теле.",
        "Совместная жизнь — постоянный мозговой штурм: путешествия, идеи, смена декораций.",
        "Риск — избегание серьёзных разговоров «на потом», пока проблемы не накопятся критически.",
        "Вместе они блистают в обществе — умные, остроумные. Наедине важно найти то, что держит крепче слов.",
    ],
    "воздух+вода": [
        "{A} говорит о чувствах — {B} их переживает. Эта разница в глубине создаёт и притяжение, и пропасть.",
        "Интуиция {B} дополняет логику {A}: {B} чувствует то, что {A} ещё только формулирует.",
        "{A} иногда кажется {B} поверхностным, хотя за лёгкостью воздуха скрывается своя форма глубины.",
        "{B} нуждается в эмоциональном присутствии, которое для {A} — непривычная территория.",
        "Когда {A} в хорошем настроении — он вытаскивает {B} из самых тёмных омутов.",
        "В творческих сферах эта пара может создавать нечто выдающееся: чувство {B} плюс форма {A}.",
        "Главная опасность — {B} привязывается глубже, чем {A} успевает осознать.",
        "Когда синхронизация найдена — один из самых стимулирующих союзов: ни скучно, ни слишком тяжело.",
    ],
    "вода+вода": [
        "{A} и {B} понимают друг друга без слов — это одновременно дар и ловушка.",
        "Эмоциональная глубина этого союза редкая. Они знают, что такое настоящая уязвимость.",
        "Созависимость — главный риск: {A} и {B} могут настолько срастись, что перестанут понимать, где один, а где другой.",
        "Сексуальная близость здесь больше чем физика — это телепатия.",
        "Оба чувствительны к критике, оба умеют обижаться надолго. Прощение — искусство, которому нужно учиться намеренно.",
        "Кризисы переживают вместе очень тяжело — два водных знака усиливают тревогу друг друга.",
        "Когда в гармонии — ощущение дома, которого не было нигде раньше. В конфликте — эмоциональный шторм.",
        "Семья и близкие — центр их мира. Этот союз строится вокруг любви, а не карьеры.",
    ],
    "земля+огонь": [
        "{A} обеспечивает {B} якорь, который тот так яростно отвергает — и так отчаянно ищет.",
        "Практичный {A} смотрит на порывы {B} с тихим восхищением и тихим ужасом одновременно.",
        "{B} заряжает {A} энергией, которой тому всегда не хватало для воплощения планов.",
        "Финансово они противоположны: {A} строит подушку безопасности, {B} её тратит.",
        "Физическая близость у них неожиданно сильная: земля медленна, но надёжна; огонь ярок, но нуждается в опоре.",
        "Главная точка роста — {A} учится у {B} решительности, {B} учится у {A} последовательности.",
        "{A} устаёт от темпа {B}, но признаёт: без него жизнь была бы слишком предсказуемой.",
        "Они дополняют друг друга как каминная решётка и огонь — вместе красиво и безопасно.",
    ],
    "воздух+огонь": [
        "{A} обдумывает — {B} уже делает. В этой разнице скоростей больше совместимости, чем кажется.",
        "{B} питает {A} вдохновением, а {A} даёт {B} концепцию, которой так не хватает его порывам.",
        "Социально эта пара блистает: остроумие {A} плюс харизма {B} притягивают людей.",
        "{A} умеет успокоить {B} в моменты ярости — через логику, которая неожиданно работает.",
        "В творческих проектах — взрывная команда: идеи {A} плюс энергия {B} дают результат быстро.",
        "Главная ловушка — {A} анализирует слишком долго, {B} обижается на нерешительность.",
        "{B} воспринимает рациональность {A} как равнодушие — важно объяснить, что это другой язык любви.",
        "Их конфликты короткие и шумные — оба не умеют держать обиду, и это реальное преимущество.",
    ],
    "вода+огонь": [
        "{A} чувствует {B} насквозь — и это пугает {B} до ужаса, хотя именно этого он всегда хотел.",
        "Интуиция {A} дополняет инстинкт {B}: вместе они принимают решения, которые другие принимают за гениальность.",
        "{B} вытаскивает {A} из скорлупы — мягко, через огонь, который согревает, а не сжигает.",
        "Сексуальная химия здесь одна из сильнейших в зодиаке: страсть {B} встречает глубину {A}.",
        "Эмоциональные качели: когда хорошо — лучше не бывает; когда плохо — оба не знают, как выбраться.",
        "{A} учит {B} чувствовать. {B} учит {A} действовать. Обмен навыками — реальный и глубокий.",
        "Главный страх {A} — быть брошенным в момент уязвимости. {B} должен это понять.",
        "Если оба готовы работать над союзом — это одна из самых трансформирующих пар зодиака.",
    ],
    "вода+земля": [
        "{A} находит в {B} то, чего так долго искал: твёрдость, надёжность, присутствие без слов.",
        "Практичность {B} никогда не кажется {A} холодной — за ней чувствуется забота.",
        "Этот союз строится медленно и на всю жизнь. Быстрой страсти нет, но есть нечто более редкое — покой.",
        "{A} иногда нуждается в эмоциональном разговоре, который {B} не умеет вести — главный системный конфликт.",
        "В финансах {B} стабилизирует {A}: хаотичные траты воды обретают форму рядом с практичностью земли.",
        "Физически это чувственная и медленная близость — никакой спешки, много внимания к деталям.",
        "{B} иногда не понимает, почему {A} так переживает из-за мелочей — нужно объяснять язык своих эмоций.",
        "Семья, дом, традиции — всё это для них не пустые слова. Этот союз создаёт корни.",
    ],
    "воздух+земля": [
        "{A} витает в облаках, {B} стоит на земле. Между ними постоянное притяжение и непонимание.",
        "Идеи {A} без реализации — ничто. {B} умеет воплощать, а {A} умеет вдохновлять.",
        "{B} воспринимает непостоянство {A} как ненадёжность, {A} воспринимает стабильность {B} как скуку.",
        "В совместных проектах эффективны: {A} придумывает, {B} делает — главное, чтобы роли были приняты.",
        "Социально {A} вводит {B} в новые круги, которые тот сам никогда бы не нашёл.",
        "Быт — камень преткновения: {A} считает порядок необязательным, {B} без него не может работать.",
        "Эмоционально {B} хочет конкретных проявлений любви, {A} предпочитает слова.",
        "Когда оба принимают разность подходов, получается пара, которая умеет и мечтать, и делать.",
    ],
    "вода+воздух": [
        "{A} чувствует то, что {B} ещё только думает — это создаёт ощущение магии в начале отношений.",
        "Интуиция {A} и логика {B} дают полную картину мира — каждый закрывает слепое пятно другого.",
        "{B} иногда кажется {A} поверхностным — хотя за лёгкостью воздуха скрывается своя глубина.",
        "{A} нуждается в эмоциональном якоре, {B} не всегда готов им быть — нужен честный разговор.",
        "Творческий потенциал огромен: чувство {A} плюс концепция {B} — нечто, что трогает и думает.",
        "В кризисах {B} предлагает решения, {A} — поддержку. Оба нужны, но не оба это признают вовремя.",
        "Главная опасность — {A} привязывается глубже, чем {B} успевает осознать.",
        "Когда синхронизация найдена — один из самых стимулирующих союзов: ни скучно, ни слишком тяжело.",
    ],
}

RU_SAME_SIGN_POINTS: list[str] = [
    "Два {A} в одном союзе — это зеркало, которое невозможно избежать. Всё, что раздражает в партнёре — это твоё собственное отражение.",
    "Понимание здесь абсолютное: {A} знает, что чувствует другой {A}, потому что сам чувствовал это тысячу раз.",
    "Главная опасность пары {A}+{A} — усиление слабостей. Если оба склонны к одному паттерну, некому его остановить.",
    "Комфорт в этом союзе немедленный — не нужно объяснять, не нужно переводить. Это редкость.",
    "Разногласия между двумя {A} особенно трудны: оба уверены, что правы — потому что думают одинаково.",
    "Сексуально пара двух {A} часто очень слаженная: один интуитивно угадывает желания другого.",
    "Этот союз либо очень крепкий, либо нестабильный — зависит от того, насколько оба {A} проработали свои теневые стороны.",
    "Вместе они могут добиться невозможного — или вместе застрять навсегда. Разнообразие взглядов нужно создавать намеренно.",
]

RU_CLIFFHANGERS: list[str] = [
    "Но есть одна деталь в их интимной совместимости, о которой астрологи говорят шёпотом — именно она решает, продержится ли этот союз дольше трёх месяцев, и связана она с...",
    "Только вот в постели у этой пары случается то, чего не ожидает ни один из партнёров — и это меняет всё, потому что...",
    "Однако существует один скрытый аспект их синастрии, который превращает страсть в одержимость за считанные недели — речь идёт о...",
    "Но есть одна деталь, о которой астрологи молчат — именно она определяет, переживёт ли ваш союз первый кризис, и она кроется в...",
    "Однако именно здесь скрывается самое важное: в их кармической связи есть один узел, который либо связывает навсегда, либо разрывает без возврата, и это...",
    "Но за всем этим стоит один нераскрытый вопрос, который задаёт каждый из партнёров себе ночью, и ответ на него определяет всё...",
    "Только вот астрологи давно заметили один феномен в парах этих знаков, который объясняет, почему они либо женятся, либо расстаются навсегда — и он связан с...",
    "Однако именно в этот момент их история делает неожиданный поворот: есть один планетарный аспект, который делает эту пару либо неразлучной, либо несовместимой — и это...",
    "Но есть нечто, что не видно снаружи и что разрушает даже самые крепкие пары этих знаков изнутри — это связано с...",
    "Только вот один конкретный триггер превращает их нежность в холодную войну за одну ночь — и он кроется в...",
    "Однако полный натальный анализ показывает кое-что, что бросает тень на всю картину совместимости — речь о...",
    "Но именно сейчас, когда кажется, что всё понятно, астрология делает неожиданный ход: есть один аспект их карт, который меняет всё, и это...",
    "Только вот именно в этой точке большинство пар этих знаков принимают роковое решение — и оно всегда связано с...",
    "Однако есть одно, о чём ни один из партнёров не говорит вслух: это скрытый страх, который либо сближает, либо разрушает их...",
    "Но самое важное в этом союзе — то, что происходит не в первые месяцы, а спустя год-два, когда всплывает кое-что из прошлых жизней...",
    "Только вот именно в вопросе власти и контроля скрывается нечто, о чём говорить не принято, а именно...",
    "Однако один конкретный момент в их взаимодействии всегда становится точкой невозврата — и он наступает тогда, когда...",
    "Но есть ещё кое-что: кармические узлы этой пары указывают на незавершённое дело из прошлых воплощений, и пока оно не решено...",
    "Только вот именно секс раскрывает в этой паре то, что не видно в обычной жизни — один паттерн, который определяет всю динамику власти...",
    "Однако полный разбор синастрии обнаруживает нечто неожиданное: у этих двух знаков есть общая уязвимость, которую они скрывают даже от себя...",
    "Но именно здесь начинается самое интересное: есть один транзит, который активируется в этой паре каждые 18 месяцев и переворачивает всё...",
    "Только вот в их прогрессированных картах видно нечто, что большинство астрологов не упоминают клиентам — слишком острая правда...",
    "Однако один архетипический конфликт, записанный в их натальных картах, будет возвращаться снова и снова, пока они не осознают...",
    "Но есть один специфический способ, которым эта пара разрушает друг друга, сами того не желая — и он всегда начинается с...",
    "Только вот именно в кризисных точках Луны этой пары случается нечто необъяснимое — паттерн, который видели все астрологи, но мало кто решился описать...",
    "Однако именно здесь скрыт ключ к пониманию, почему эта пара может быть либо вечной, либо разрушительной — ответ в их восьмом доме синастрии...",
    "Но кое-что в их сексуальной карте говорит о скрытых желаниях, которые ни один из партнёров не озвучивает — и именно они определяют...",
    "Только вот именно этот аспект Марса в их синастрии превращает нежность в контроль быстрее, чем любой другой фактор...",
    "Однако есть один вопрос, который эта пара должна задать себе до того, как двигаться дальше — и ответ требует астрологического разбора...",
    "Но именно здесь их история могла бы закончиться, если бы не один скрытый ресурс, который активируется только при определённом условии...",
    "Только вот есть одна вещь, которую оба партнёра чувствуют, но не могут объяснить — она напрямую связана с кармической историей их союза...",
    "Однако полный анализ их Луны и Венеры открывает нечто, что меняет интерпретацию всей совместимости — и это касается...",
]

RU_TITLE_TEMPLATES: list[str] = [
    "Совместимость {gen_a} и {gen_b} — астроразбор 2026 | Synastry AI",
    "Совместимость {gen_a} и {gen_b}: любовь и отношения | Synastry AI",
    "{name_a} и {name_b}: совместимость в любви 2026 | Synastry AI",
    "Совместимость {gen_a} и {gen_b} — натальный анализ | Synastry AI",
    "{name_a} + {name_b}: совместимость знаков | Synastry AI",
]

RU_DESC_TEMPLATES: list[str] = [
    "Подробный астрологический анализ совместимости {gen_a} и {gen_b} в любви, отношениях и сексе. Сильные и слабые стороны союза.",
    "Совместимость {gen_a} и {gen_b}: разбор синастрии, натальных карт, кармических связей и прогноз на 2026 год.",
    "Что ждёт пару {name_a} и {name_b}? Натальный разбор совместимости в любви, браке и близости от Synastry AI.",
    "Астрологический прогноз для пары {name_a} + {name_b}: совместимость характеров, стихий и кармических узлов.",
    "Полная совместимость {gen_a} и {gen_b}: любовь, секс, дружба и деньги — честный астрологический анализ.",
    "{name_a} и {name_b}: насколько вы совместимы? Разбор синастрии, аспектов Венеры и Марса, прогноз отношений.",
]

# ═══════════════════════════════════════════════════════════════════════
# ENGLISH CONTENT
# ═══════════════════════════════════════════════════════════════════════

EN_ELEMENT_POINTS: dict[str, list[str]] = {
    "fire+fire": [
        "Two fire signs bring immediate electricity — the chemistry between {A} and {B} is visceral and mutual. The challenge is that both need to lead, and neither ever learned to follow.",
        "{A} sees in {B} a mirror of their own intensity. At first this feels validating; over time it becomes a quiet competition over who burns the brightest.",
        "Arguments in this pairing are explosive and short — neither {A} nor {B} knows how to hold a grudge for long. The make-ups are just as intense as the blow-ups.",
        "Sexually, {A} and {B} are one of the most combustible pairings in the zodiac. Physical chemistry is rarely the problem here.",
        "The real test for this couple is shared resources: both tend to spend with confidence rather than caution, and financial friction can accumulate fast.",
        "Together {A} and {B} radiate a magnetic energy that draws people in. Separately, they're strong. Together, they're a force — or a fire hazard.",
        "The ego dynamic is this pairing's defining challenge: both signs believe, at some level, that they deserve the starring role.",
        "When they align their ambitions instead of competing, {A} and {B} can achieve things that seem genuinely impossible to everyone watching.",
    ],
    "fire+earth": [
        "{A}'s impulsiveness runs directly into {B}'s need for stability — and that friction is both the attraction and the seed of every recurring argument.",
        "{B} quietly provides the infrastructure that {A}'s ideas need to actually land. {A} gives {B} the nerve to step outside their carefully constructed routines.",
        "Money is a pressure point: {A} spends on instinct, {B} builds reserves methodically. Without a shared financial philosophy, this becomes the argument they always circle back to.",
        "In the long run, {B} may find {A}'s pace genuinely exhausting — not because they don't love them, but because they're built for endurance, not sprinting.",
        "The physical connection between these two is often surprisingly strong: earth's patience meets fire's heat in a combination that tends to satisfy both.",
        "{A} reads {B}'s caution as timidity. {B} reads {A}'s boldness as recklessness. They're both partially right, and that's actually fine.",
        "When they build something together — a business, a home, a shared project — the result tends to outlast every other couple's attempt.",
        "{A} teaches {B} to want things out loud. {B} teaches {A} that wanting isn't enough — you have to show up consistently. Both lessons are necessary.",
    ],
    "fire+air": [
        "{A} and {B} create a relationship that has no off switch — conversations, plans, debates, laughter. Boredom is structurally impossible between them.",
        "Air fuels fire: {B} knows exactly how to appreciate {A} in ways that make them feel truly seen, which only makes {A} burn hotter.",
        "The intellectual connection here is genuine, but there's a timing gap: {A} wants to move now, {B} is still running through the options.",
        "This pairing wears well in public — they're entertaining, warm, and interesting together. Behind closed doors the dynamic is more complicated.",
        "{B} can come across as emotionally detached to {A}, who craves a warmer response. {A} can seem overwhelming to {B}, who values their own interior quiet.",
        "Shared adventures and new experiences are the glue of this relationship. Routine is genuinely threatening to both of them.",
        "Their arguments tend to be brief and pointed — {B} leads with logic, {A} leads with heat, and somehow this works better than it sounds.",
        "Freedom matters to both: neither wants to be owned, and that mutual understanding creates a kind of trust that heavier relationships often lack.",
    ],
    "fire+water": [
        "{A} and {B} represent one of astrology's classic contradictions — fire wants to expand, water wants to deepen. The pull between them is real but requires constant translation.",
        "{B}'s emotional depth both unsettles and captivates {A}. {A} has never quite felt this known before — and never quite felt this exposed.",
        "The core disconnect: {A} responds to the world through action, {B} through feeling. The same event can hit them completely differently.",
        "{B} reads {A} without words — a gift that {A} finds alternately magical and invasive, especially when the reading is accurate.",
        "Sexually, this pairing tends to be intense. {B}'s intuition meets {A}'s passion in a combination that often surprises both of them.",
        "When {A} gets loud, {B} goes quiet — and the silence becomes heavier than any argument. This pairing needs a protocol for cooling down.",
        "{B} needs emotional security that {A} doesn't always know how to deliver. {A} needs space that {B} can experience as abandonment.",
        "If {A} learns to slow down and {B} learns to speak up, this becomes one of the genuinely rare pairings: deep and alive at the same time.",
    ],
    "earth+earth": [
        "{A} and {B} build a relationship the way they build everything else — carefully, solidly, and with an eye toward whether it will still be standing in twenty years.",
        "Financial compatibility here is exceptional. Both understand the difference between spending and investing, and they rarely fight about money.",
        "The risk in this pairing is that stability becomes stagnation. Without deliberate effort to introduce something new, the relationship can quietly calcify.",
        "Physical affection is a primary love language for both {A} and {B} — they need to be touched, held, and physically present with each other.",
        "Both are stubborn. Both are usually correct. Neither apologizes first. Conflicts in this pairing can last days — but so does the repair.",
        "There's a rare quality of safety in this relationship. {A} and {B} know that whatever comes, the other one isn't going anywhere.",
        "They can spend years discussing the same major life change — the move, the career pivot, the renovation — without pulling the trigger. Inertia is their shared weakness.",
        "From the outside this pairing can look boring. From the inside it's something most people quietly wish they had.",
    ],
    "earth+air": [
        "{A} wants structure; {B} wants room to breathe. The unspoken contract between them: you don't cage me, I don't disappear on you.",
        "{B}'s mind genuinely impresses {A}. The ideas that live in air need earth to make them real — and {A} is very good at making things real.",
        "{B} can experience {A}'s routines as constriction. {A} can experience {B}'s inconsistency as flakiness. Both perceptions are partially accurate.",
        "Daily life is where this pairing generates friction: {A} runs on systems and predictability, {B} runs on improvisation and novelty.",
        "Conversations between {A} and {B} can run for hours — {B} generates ideas, {A} stress-tests them. It's a genuinely productive dynamic.",
        "Socially, {B} pulls {A} into circles and conversations they would never find alone, which slowly expands {A}'s world in ways they don't always acknowledge.",
        "{A} tends to express love through consistency and acts of service. {B} tends to express it through words and attention. Learning each other's dialect takes time.",
        "When both accept the fundamental difference in their approaches, this becomes one of the more effective combinations: vision plus execution.",
    ],
    "earth+water": [
        "{A} and {B} find in each other a rare thing — genuine understanding without performance. Earth doesn't fear the depth of water.",
        "{B} has a way of softening {A} in places where {A} didn't realize they'd gone rigid. Water finds the cracks in stone.",
        "Financial decisions in this pairing tend to be sound: {A}'s pragmatism combined with {B}'s intuition produces unusually good outcomes.",
        "The primary risk is codependency. {B} can become structurally necessary to {A}'s emotional functioning, and {A} can become the only safe harbor {B} trusts.",
        "In a crisis, {A} is the stable ground that {B} desperately needs. The reliability of earth is genuinely therapeutic for water signs.",
        "Physical intimacy here tends to be unhurried and attentive — both signs have an instinct for what the other needs.",
        "{A} sometimes seems cold to {B} in moments of distress. What reads as coldness is usually {A} trying to solve the problem rather than sit with the feeling.",
        "This is one of the more quietly durable pairings in astrology — not spectacular, but built for the long run in ways that many flashier couples aren't.",
    ],
    "air+air": [
        "{A} and {B} meet primarily in the mind — the emotional dimension of their relationship develops later, and sometimes it never fully arrives.",
        "Intellectual compatibility here is nearly perfect. They finish each other's thoughts, trade references, and argue about ideas for sport.",
        "Both signs tend to process feelings through analysis rather than expression. This creates harmony until one of them actually needs to be held.",
        "Freedom is non-negotiable for both {A} and {B}. The fact that they both understand this creates a mutual trust that many couples never develop.",
        "The relationship's social presence is notable — {A} and {B} together are articulate, interesting, and entertaining. Privately, they need to remember to be vulnerable.",
        "Life with these two is rarely static: they're constantly generating new ideas, new plans, new projects. Whether they follow through is another question.",
        "The danger in this pairing is collective avoidance — both are skilled at talking around difficult feelings rather than through them.",
        "When they do find depth together, it tends to involve creative or intellectual work — building something meaningful is how they most fully bond.",
    ],
    "air+water": [
        "{A} speaks about feelings; {B} lives inside them. This gap in depth creates both the attraction and the ongoing difficulty.",
        "{B}'s intuition pairs with {A}'s analysis in a way that's genuinely complementary — {B} senses what {A} hasn't yet articulated.",
        "{A} can come across as emotionally superficial to {B}, who experiences the world in full feeling. What {B} reads as shallowness is usually just a different register.",
        "{B} needs emotional presence that doesn't come naturally to {A}, who often defaults to problem-solving when sitting with the feeling would help more.",
        "At {A}'s best, they pull {B} up and out of their own depths with a lightness that's actually healing. Air carries water without knowing it.",
        "Creatively, this pairing can be exceptional: {B}'s feeling instinct combined with {A}'s capacity for form and concept produces work with both resonance and clarity.",
        "The primary danger here is asymmetric attachment — {B} tends to bond at a depth and speed that {A} isn't tracking, which sets up a painful mismatch.",
        "When they find their sync, this becomes one of the more stimulating combinations: never dull, never overwhelming.",
    ],
    "water+water": [
        "{A} and {B} understand each other without explanation — a gift that's also a trap, because silence begins to carry more weight than either can manage.",
        "The emotional depth of this pairing is uncommon. Both know what real vulnerability looks like, and neither flinches from it in the other.",
        "Codependency is the central risk: {A} and {B} can merge so completely that individual identity starts to blur.",
        "Sexually, this pairing tends to operate like a feedback loop — each sensing and responding to the other's needs in ways that feel borderline telepathic.",
        "Both signs carry sensitivity to criticism and a capacity for extended silence as punishment. Forgiveness in this pairing requires deliberate intention.",
        "In crisis, two water signs together can amplify each other's anxiety rather than stabilize it. They need to develop grounding practices separately.",
        "When they're aligned, no other pairing creates the same sense of being truly at home with another person. When they're not — the storm is oceanic.",
        "Family, legacy, and belonging sit at the center of both their lives. This relationship is built around love in a way that career-first partnerships rarely match.",
    ],
    "earth+fire": [
        "{A} is the anchor that {B} resists and desperately needs at the same time.",
        "Practical {A} watches {B}'s impulsive moves with a mixture of admiration and quiet alarm.",
        "{B} charges {A} with energy they've always needed to turn their careful plans into action.",
        "Financially they operate on opposite instincts: {A} builds reserves, {B} deploys them — sometimes without consulting {A}.",
        "The physical connection in this pairing is unexpectedly strong. Earth's patience gives fire somewhere to land.",
        "The growth edge: {A} learns decisive action from {B}; {B} learns follow-through from {A}.",
        "{A} occasionally burns out on {B}'s pace. And yet life without that pace feels strangely flat.",
        "Together they function like a well-designed engine: one generates the heat, the other contains and channels it.",
    ],
    "air+fire": [
        "{A} deliberates; {B} is already moving. The gap in timing holds more compatibility than it initially appears.",
        "{B} gives {A} inspiration. {A} gives {B}'s momentum a direction it was missing.",
        "Socially this pairing is magnetic — {A}'s wit combined with {B}'s presence tends to fill a room.",
        "{A} can talk {B} down from a genuine fury using logic alone — a skill most people would find impossible.",
        "On collaborative projects they can be surprisingly fast: {A}'s concept plus {B}'s energy produces results ahead of schedule.",
        "The sticking point: {A} takes longer to commit than {B} finds comfortable, and {B}'s impatience reads to {A} as pressure.",
        "{B} sometimes reads {A}'s rationality as indifference. The reality is that {A} expresses care differently — worth explaining explicitly.",
        "Arguments tend to blow over quickly: neither holds onto conflict naturally, which is one of this pairing's cleaner advantages.",
    ],
    "water+fire": [
        "{A} reads {B} with unsettling accuracy — which terrifies {B}, because this is exactly what they've always wanted.",
        "{A}'s intuition and {B}'s instinct combine into a decision-making process that other people experience as uncanny.",
        "{B} draws {A} out of isolation — not through force, but through a warmth that makes the outside world feel survivable.",
        "Sexually, this is one of the more explosive pairings: {B}'s passion lands directly on {A}'s emotional depth.",
        "The dynamic swings hard: when it's good, nothing compares to it. When it breaks down, neither knows how to find the exit.",
        "{A} teaches {B} to feel. {B} teaches {A} to act. The exchange of capacities is real and lasting.",
        "{A}'s deepest fear is being left at the moment of vulnerability. {B} needs to understand this — and resist using it.",
        "If both are willing to do the relational work, this pairing has transformational potential that more compatible-seeming pairs rarely achieve.",
    ],
    "water+earth": [
        "{A} finds in {B} the solidity they've been quietly searching for — reliability without conditions.",
        "{B}'s practicality never reads as cold to {A}. The structure is itself a form of care, and {A} understands this.",
        "This relationship builds slowly and tends to last. There's no early fireworks, but there's something rarer — real peace.",
        "The friction point: {A} occasionally needs an emotional conversation that {B} isn't wired to initiate. This is the pairing's one recurring gap.",
        "Financially, {B} provides stability that helps {A}'s diffuse energy actually accumulate into something.",
        "Physical intimacy here is slow, attentive, and genuinely caring — both parties have an instinct for presence.",
        "{B} sometimes doesn't understand why {A} is so affected by something seemingly small. Learning to ask before interpreting is important.",
        "Home, family, rootedness — none of these are abstract concepts for either partner. This pairing creates something durable.",
    ],
    "air+earth": [
        "{A} lives in concepts; {B} lives in materials. The gap is real, but so is the complementarity.",
        "{A}'s ideas without execution are incomplete. {B} knows how to execute. This is a workable division of labor — if both accept it.",
        "{B} reads {A}'s variability as unreliability. {A} reads {B}'s consistency as lack of imagination. Neither reading is entirely fair.",
        "Domestic life generates friction: {A} treats order as optional, {B} experiences disorder as genuinely stressful.",
        "Professionally and creatively, this combination can be very effective: {A} generates the vision, {B} makes it happen.",
        "Socially, {A} brings {B} into new territory — conversations, people, and experiences that {B} would never encounter alone.",
        "{B} expresses love through actions. {A} expresses it through words. Understanding this difference prevents a lot of unnecessary hurt.",
        "When both partners accept the fundamental difference in their operating systems, this becomes one of the more practical pairings in the zodiac.",
    ],
    "water+air": [
        "{A} senses what {B} is still trying to articulate — which creates a quality of early-stage magic that's hard to explain to anyone outside the relationship.",
        "{A}'s emotional intelligence and {B}'s analytical intelligence form a genuinely complementary pair: each covers the other's blind spot.",
        "{B} can seem emotionally lightweight to {A}, who experiences the world at full emotional volume. What {B} calls equanimity, {A} can experience as absence.",
        "{A} needs emotional presence and depth of connection. {B} needs autonomy and intellectual engagement. Both needs are legitimate — the question is whether both can be met.",
        "At their best, {B} brings {A} out of emotional heaviness with a lightness that genuinely helps. Levity, offered at the right moment, is a genuine form of support.",
        "Creative collaborations between these two can produce work of unusual range — feeling and form in balance.",
        "The attachment asymmetry is the main hazard: {A} tends to bond faster and deeper than {B} realizes, and the gap in intensity can cause real pain.",
        "When they find their equilibrium, this pairing produces something neither sign achieves easily alone: depth with ease.",
    ],
}

EN_SAME_SIGN_POINTS: list[str] = [
    "Dating another {A} is like meeting your own reflection — the instant recognition is real, and so are all the habits you've been quietly hoping a partner wouldn't notice.",
    "Two {A}s never have to explain themselves to each other. The ease of this is real, and so is the risk: without friction, some growth simply doesn't happen.",
    "Your shared strengths amplify in this pairing — and so do your shared weaknesses. If {A} tends toward a particular pattern, two of them together reinforce it rather than challenge it.",
    "Conflict between two {A}s hits differently than other pairings: you both know exactly which pressure points will land, because they're the same ones that affect you.",
    "The sexual connection here tends to be naturally attuned — you know what the other person wants because it's what you want.",
    "The growth challenge is that you both have the same relationship with discomfort. If {A} tends to avoid something, neither partner is likely to push the other through it.",
    "Two {A}s can go far together — or they can loop indefinitely in the same dynamic. The deciding variable is how much self-awareness each person has brought into the relationship.",
    "What outsiders see as an oddly well-matched couple is actually two people who finally don't have to translate themselves. The relief is genuine.",
]

EN_CLIFFHANGERS: list[str] = [
    "But there's one detail about their sexual compatibility that most astrologers won't say aloud — and it's the single factor that determines whether this union survives the six-month mark, rooted in...",
    "Yet what almost no couples therapist or astrologer will tell you about this pairing lies in their composite eighth house — and once you see it, everything shifts, because...",
    "However, one specific Mars-Venus aspect in their synastry quietly turns attraction into fixation within weeks — and it traces back to...",
    "But a deeper read of their natal charts reveals something that upends the standard compatibility narrative for these two signs — specifically...",
    "The real story of this pairing only becomes visible eighteen months in, when a particular planetary transit activates a pressure point that's been dormant since day one...",
    "Yet there's one thing neither partner ever says out loud, even though both feel it — a shared vulnerability that either binds them permanently or eventually tears them apart, and it lives in...",
    "But astrologers who specialize in long-term compatibility have noticed a consistent pattern in this pairing that explains why they either marry or end things abruptly — it comes down to...",
    "However, the deeper synastry reading reveals something surprising about their power dynamic — a pattern that most couples in this pairing don't identify until it's already been running for years...",
    "Yet there's one specific trigger that transforms their tenderness into a cold war overnight — and understanding it requires looking at something most people overlook in compatibility readings...",
    "But the full natal analysis surfaces a detail that quietly rewrites everything — one that most practitioners don't mention because it requires a level of honesty most clients aren't ready for...",
    "However, something in their progressed charts tells a story about this pairing that the standard sun-sign analysis misses entirely — and it has to do with...",
    "Yet the chart doesn't lie about this one thing: there's an aspect in their synastry that will activate at a predictable point in the relationship, and when it does...",
    "But what actually determines whether this pairing lasts isn't what either partner thinks it is — it's an 8th house placement that most people have never looked at...",
    "However, one archetype embedded in both charts keeps surfacing in the relationship — an unresolved pattern that neither partner can resolve alone, connected to...",
    "Yet the sexual dimension of this pairing contains something that upends the public story these two tell about themselves — a private dynamic rooted in...",
    "But the composite chart shows something that's easy to miss at first: a hidden strength that only activates under pressure — specifically...",
    "However, there's a karmic thread running through this connection that most astrologers note privately and rarely discuss openly, because it suggests...",
    "Yet one specific aspect of their Moon synastry reveals a recurring cycle in this relationship — one that follows a predictable rhythm and always returns to...",
    "But ask any astrologer who specializes in relationship charts what they notice first about this pairing, and they'll point to one thing: a placement that predicts...",
    "However, the real compatibility question for this pairing isn't whether they love each other — it's whether they can navigate a specific pattern that emerges around month nine...",
    "Yet there's a shadow element in their synastry that tends to surface only when the relationship feels most secure — and understanding it requires looking at...",
    "But the 12th house of their composite chart holds something that explains the inexplicable pull between them — a connection that predates this lifetime and shows up as...",
    "However, one Venus placement in this synastry creates a dynamic that feels like intimacy but can function as control — distinguishing between the two requires...",
    "Yet the nodal axis of their connection points to a specific piece of unfinished business — something that will keep recurring until both partners consciously address...",
    "But the astrology of long-term commitment for this pairing hinges on something most compatibility guides never mention: a Saturn aspect that determines...",
    "However, something about their Mars synastry creates an escalation pattern that neither person plans for — it only becomes visible when you look at...",
    "Yet what makes this pairing genuinely unusual isn't the compatibility score — it's one specific placement that overrides almost everything else in the chart...",
    "But there's a particular moment in every relationship between these two signs where a choice gets made — usually unconsciously — that determines the entire trajectory...",
    "However, the deeper question for this pairing isn't about elements or modalities — it's about one hidden need that neither partner can meet for themselves, which means...",
    "Yet the astrology is unusually clear about one thing: there's a window in this relationship's timeline where everything becomes possible, and if it's missed...",
    "But the thing that actually holds this pairing together long-term isn't what's visible in the early months — it's something that only emerges after the first real crisis...",
    "However, one placement in the composite seventh house reveals why this pairing often feels fated — a quality that most couples never develop, rooted in...",
]

EN_TITLE_TEMPLATES: list[str] = [
    "{name_a} and {name_b} Compatibility — Natal Reading 2026 | Synastry AI",
    "{name_a} & {name_b} Love Compatibility — Synastry Reading | Synastry AI",
    "Are {name_a} and {name_b} Compatible? Full Analysis | Synastry AI",
    "{name_a} and {name_b} Synastry: Love & Relationships | Synastry AI",
    "{name_a} + {name_b} Compatibility — Astrology 2026 | Synastry AI",
]

EN_DESC_TEMPLATES: list[str] = [
    "In-depth astrological compatibility analysis for {name_a} and {name_b} in love, sex, and relationships. Key strengths, friction points, and 2026 outlook.",
    "Are {name_a} and {name_b} a good match? Full natal chart synastry, Venus-Mars aspects, karmic connections, and relationship forecast.",
    "{name_a} and {name_b} compatibility: synastry breakdown, karmic bonds, and honest insights into whether this pairing has staying power.",
    "Full synastry reading for {name_a} and {name_b}: emotional chemistry, sexual compatibility, long-term potential, and key challenges.",
    "What astrology actually says about {name_a} and {name_b} — synastry, composite chart patterns, and a clear-eyed 2026 forecast.",
    "{name_a} meets {name_b}: complete astrological compatibility report including Venus aspects, karmic nodes, and a 12-month relationship outlook.",
]

# ═══════════════════════════════════════════════════════════════════════
# ENGINE
# ═══════════════════════════════════════════════════════════════════════

def generate_entry(sign_a: dict, sign_b: dict, cfg: dict) -> dict:
    pair_id = f"{sign_a['slug']}-{sign_b['slug']}"
    rng = random.Random(pair_id)

    name_a = sign_a["name"]
    name_b = sign_b["name"]
    gen_a  = sign_a.get("name_gen", name_a)
    gen_b  = sign_b.get("name_gen", name_b)

    # Title
    title = rng.choice(cfg["title_templates"]).format(
        name_a=name_a, name_b=name_b, gen_a=gen_a, gen_b=gen_b
    )
    # Description
    description = rng.choice(cfg["desc_templates"]).format(
        name_a=name_a, name_b=name_b, gen_a=gen_a, gen_b=gen_b
    )

    # Compatibility points
    if sign_a["slug"] == sign_b["slug"]:
        pool = [p.format(A=name_a, B=name_b) for p in cfg["same_sign_points"]]
    else:
        key = f"{sign_a['element']}+{sign_b['element']}"
        raw = cfg["element_points"].get(key, list(cfg["element_points"].values())[0])
        pool = [p.format(A=name_a, B=name_b) for p in raw]

    if len(pool) < 3:
        pool = pool * 3
    points = rng.sample(pool, 3)

    cliffhanger = rng.choice(cfg["cliffhangers"])

    return {
        "id": pair_id,
        "sign_a": {"slug": sign_a["slug"], "name": name_a},
        "sign_b": {"slug": sign_b["slug"], "name": name_b},
        "title": title,
        "description": description,
        "compatibility_points": points,
        "cliffhanger": cliffhanger,
    }


def write_json(data: list[dict], path: Path) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    size_kb = path.stat().st_size / 1024
    avg_len = sum(len(p) for e in data for p in e["compatibility_points"]) / (len(data) * 3)
    print(f"[OK] {path.name}: {len(data)} entries, avg point {avg_len:.0f} chars, {size_kb:.1f} KB")


def main() -> None:
    base = Path(__file__).parent.parent

    CONFIGS = {
        "ru": {
            "signs": SIGNS_RU,
            "element_points": RU_ELEMENT_POINTS,
            "same_sign_points": RU_SAME_SIGN_POINTS,
            "cliffhangers": RU_CLIFFHANGERS,
            "title_templates": RU_TITLE_TEMPLATES,
            "desc_templates": RU_DESC_TEMPLATES,
            "out": base / "data" / "compatibility_ru.json",
        },
        "en": {
            "signs": SIGNS_EN,
            "element_points": EN_ELEMENT_POINTS,
            "same_sign_points": EN_SAME_SIGN_POINTS,
            "cliffhangers": EN_CLIFFHANGERS,
            "title_templates": EN_TITLE_TEMPLATES,
            "desc_templates": EN_DESC_TEMPLATES,
            "out": base / "data" / "compatibility_en.json",
        },
    }

    for lang, cfg in CONFIGS.items():
        data = [
            generate_entry(a, b, cfg)
            for a, b in itertools.product(cfg["signs"], cfg["signs"])
        ]
        write_json(data, cfg["out"])

    print(f"[OK] Both JSON files written to {base / 'data'}")


if __name__ == "__main__":
    main()
