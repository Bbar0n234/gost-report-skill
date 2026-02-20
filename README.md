# gost-report-skill

Claude Code skill для автоматического оформления отчётов по лабораторным работам в соответствии с ГОСТ 7.32.

## Что делает

- LLM генерирует отчёт в Markdown
- Скрипт собирает .docx с правильными стилями (Times New Roman 14pt, отступы, поля по ГОСТ) и титульным листом
- Титульный лист заполняется автоматически из YAML-метаданных

## Пререквизиты

- [Pandoc](https://pandoc.org/) >= 3.1.12
- Python >= 3.10
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

### Формат Markdown

Отчёт начинается с YAML front matter:

```yaml
---
title: "Лабораторная работа №3"
teacher_title: "канд. техн. наук, доцент"
teacher_name: "И.И. Петров"
lab_number: "3"
lab_title: "Исследование характеристик системы"
discipline: "Операционные системы"
group: "3234к"
student_name: "С.А. Феоктистов"
department: "Кафедра №33"
---

# Теоретическая часть

Текст отчёта...

\newpage

# Выводы

Текст выводов...
```

## Кастомизация титульного листа

Титульный лист встроен в `gost-lab-report/templates/reference.docx`. Для адаптации под свой вуз:

1. Откройте `reference.docx` в LibreOffice/Word
2. Замените титульный лист на шаблон вашего вуза
3. Вставьте плейсхолдеры `{{FIELD_NAME}}` в нужные места
4. Сохраните

Поддерживаемые плейсхолдеры: `{{TEACHER_TITLE}}`, `{{TEACHER_NAME}}`, `{{LAB_NUMBER}}`, `{{LAB_TITLE}}`, `{{DISCIPLINE}}`, `{{GROUP}}`, `{{STUDENT_NAME}}`, `{{DEPARTMENT}}`, `{{YEAR}}` (заполняется автоматически).

## Лицензия

MIT
