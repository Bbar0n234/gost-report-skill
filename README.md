# gost-report-skill

Claude Code skill для автоматического оформления отчётов по лабораторным работам в соответствии с ГОСТ 7.32.

## Что делает

- LLM-агент анализирует методичку / задание, предлагает структуру отчёта, согласовывает с пользователем
- Генерирует отчёт в Markdown
- Скрипт собирает .docx с правильными стилями (Times New Roman 14pt, отступы, поля по ГОСТ) и титульным листом
- Титульный лист заполняется автоматически из YAML-метаданных

## Пререквизиты

- [Pandoc](https://pandoc.org/) >= 3.1.12
- Python >= 3.10
- Python-пакеты: `python-docx`, `docxcompose`
- Шрифт Times New Roman

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/Bbar0n234/gost-report-skill.git
```

2. Установить Python-зависимости:
```bash
pip install python-docx docxcompose
```

3. Скопировать скилл в Claude Code:
```bash
cp -r gost-report-skill/gost-lab-report ~/.claude/skills/
```

## Использование

### С Claude Code

Скилл активируется автоматически по ключевым словам: «отчёт», «лабораторная», «оформить», «ГОСТ».

Пример: *«Оформи отчёт по лабораторной работе №3 по дисциплине Операционные системы»*

### Ручная сборка

```bash
python ~/.claude/skills/gost-lab-report/scripts/build.py report.md
```

## Кастомизация титульного листа

Титульный лист встроен в `gost-lab-report/templates/reference.docx`. Для адаптации под свой вуз:

1. Откройте `reference.docx` в LibreOffice/Word
2. Замените титульный лист на шаблон вашего вуза
3. Вставьте плейсхолдеры `{{FIELD_NAME}}` в нужные места
4. Сохраните

Поддерживаемые плейсхолдеры: `{{TEACHER_TITLE}}`, `{{TEACHER_NAME}}`, `{{LAB_NUMBER}}`, `{{LAB_TITLE}}`, `{{DISCIPLINE}}`, `{{GROUP}}`, `{{STUDENT_NAME}}`, `{{DEPARTMENT}}`, `{{YEAR}}` (заполняется автоматически).

## Поддерживаемые вузы

Готовые шаблоны титульных листов (в разработке):

- *Список будет дополнен*

Если вашего вуза нет в списке — используйте инструкцию по кастомизации выше или Setup Wizard (`gost-lab-report/SETUP.md`).

## Роадмап

Подробный план развития: [docs/ROADMAP.md](docs/ROADMAP.md)
