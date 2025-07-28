
import re

with open(".\\main\\templates\\candidate\\c4\\cc4.html", "r", encoding="utf-8") as f:
    html = f.read()

if '{% load static %}' not in html:
    html = '{% load static %}\n\n' + html

# assets 경로 변환
html = re.sub(r'"assets/([^"]+)"', lambda m: f'"{{% static \'c4/assets/{m.group(1)}\' %}}"', html)

# images 경로 변환
html = re.sub(r'"images/([^"]+)"', lambda m: f'"{{% static \'c4/images/{m.group(1)}\' %}}"', html)

with open("cc4_converted.html", "w", encoding="utf-8") as f:
    f.write(html)
