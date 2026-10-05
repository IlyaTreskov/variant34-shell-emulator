def run_startup_script(path, shell, output):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as exc:
        output(f"startup error: {exc}")
        return False

    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        output(f"$ {line}")
        ok, message = shell.execute(line)
        if message:
            output(message)
        if not ok:
            output(f"startup stopped at line {number}")
            return False
        if shell.should_exit:
            return True
    return True
