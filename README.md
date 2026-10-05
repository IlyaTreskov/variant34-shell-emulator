# Эмулятор командной оболочки ОС — вариант 34

Практическая работа №1 по дисциплине **«Конфигурационное управление»**.

Проект реализует графический эмулятор UNIX-подобной командной строки с виртуальной файловой системой (VFS), полностью находящейся в памяти.

Язык: **Python 3**  
GUI: **Tkinter**

## Возможности

1. **REPL и GUI** — окно `Эмулятор - [username@hostname]`, парсер аргументов в кавычках, обработка ошибок, `exit`.
2. **Конфигурация** — `--vfs`, `--script`, `--debug-config`.
3. **VFS** — XML, UTF-8, base64, работа в памяти, `vfs-save`.
4. **Основные команды** — `ls`, `cd`, `tac`, `head`, `history`.
5. **Дополнительная команда** — `mv`.

## Структура

```text
.
├── .gitignore
├── README.md
├── run.bat
├── run.sh
├── src/
│   ├── main.py
│   └── emulator/
│       ├── __init__.py
│       ├── config.py
│       ├── gui.py
│       ├── parser.py
│       ├── shell.py
│       ├── startup.py
│       └── vfs.py
├── tests/
├── examples/
│   ├── startup/
│   └── vfs/
└── scripts/
```

## Требования

- Python 3.10+
- Tkinter
- сторонние библиотеки не требуются

## Запуск

Windows:

```bat
run.bat --vfs examples\vfs\demo.xml
```

Прямой запуск:

```bash
python src/main.py --vfs examples/vfs/demo.xml
```

Полная демонстрация:

```bash
python src/main.py --vfs examples/vfs/demo.xml --script examples/startup/full_demo.txt --debug-config
```

Windows:

```bat
scripts\run_full_demo.bat
```

## Команды

- `ls [PATH]`
- `cd [PATH]`
- `tac FILE`
- `head [-n N] FILE`
- `history`
- `mv SOURCE DESTINATION`
- `vfs-save PATH`
- `exit`

## Тестирование

```bash
python -m unittest discover -s tests -v
```

## Рекомендуемая история коммитов

```text
feat(repl): implement GUI loop and quoted parser
feat(config): add CLI options and startup scripts
feat(vfs): add in-memory XML virtual file system
feat(commands): implement ls cd tac head and history
feat(vfs): implement in-memory mv command
test(shell): add automated tests
docs(readme): add project documentation
```

## Что отправлять в СДО

1. URL публичного GitHub-репозитория.
2. PDF-версию `README.md`.
