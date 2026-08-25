При разработке:
1. в файле .dockerignore закомментировать строчки: <br>

static/images/*.png <br>
static/images/*.jpg <br>
static/images/*.webp

2. Перед коммитом вернуть обратно
3. Запустить файл docker_run_simple.bat
4. При внесении изменений нужно перезапустить скрипт чтобы контейнер пересобрался

При деплое написать в терминал
<b>git push dokku main</b>