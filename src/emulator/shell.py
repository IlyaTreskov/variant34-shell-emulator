from emulator.parser import ParseError, parse_command
from emulator.vfs import VFSError


class Shell:
    def __init__(self, vfs):
        self.vfs = vfs
        self.cwd = "/"
        self.history_items = []
        self.should_exit = False

    def execute(self, line):
        self.history_items.append(line)
        try:
            parts = parse_command(line)
        except ParseError as exc:
            return False, f"parse error: {exc}"
        if not parts:
            return True, ""
        command, *args = parts
        handlers = {
            "ls": self._cmd_ls,
            "cd": self._cmd_cd,
            "tac": self._cmd_tac,
            "head": self._cmd_head,
            "history": self._cmd_history,
            "mv": self._cmd_mv,
            "vfs-save": self._cmd_vfs_save,
            "exit": self._cmd_exit,
        }
        handler = handlers.get(command)
        if handler is None:
            return False, f"unknown command: {command}"
        try:
            return True, handler(args)
        except VFSError as exc:
            return False, str(exc)
        except ValueError as exc:
            return False, str(exc)

    def _cmd_ls(self, args):
        if len(args) > 1:
            raise ValueError("usage: ls [PATH]")
        path = args[0] if args else self.cwd
        node = self.vfs.get_node(path, self.cwd)
        if node["type"] != "dir":
            raise VFSError(f"not a directory: {path}")
        names = []
        for name, child in sorted(node["children"].items()):
            names.append(name + ("/" if child["type"] == "dir" else ""))
        return "\n".join(names)

    def _cmd_cd(self, args):
        if len(args) > 1:
            raise ValueError("usage: cd [PATH]")
        path = args[0] if args else "/"
        node = self.vfs.get_node(path, self.cwd)
        if node["type"] != "dir":
            raise VFSError(f"not a directory: {path}")
        self.cwd = self.vfs.normalize(path, self.cwd)
        return ""

    def _read_text_file(self, path):
        node = self.vfs.get_node(path, self.cwd)
        if node["type"] != "file":
            raise VFSError(f"not a file: {path}")
        if node["binary"]:
            raise VFSError(f"binary file: {path}")
        return node["content"]

    def _cmd_tac(self, args):
        if len(args) != 1:
            raise ValueError("usage: tac FILE")
        return "\n".join(reversed(self._read_text_file(args[0]).splitlines()))

    def _cmd_head(self, args):
        count = 10
        if len(args) == 1:
            path = args[0]
        elif len(args) == 3 and args[0] == "-n":
            try:
                count = int(args[1])
            except ValueError as exc:
                raise ValueError("head: N must be an integer") from exc
            path = args[2]
        else:
            raise ValueError("usage: head [-n N] FILE")
        return "\n".join(self._read_text_file(path).splitlines()[:count])

    def _cmd_history(self, args):
        if args:
            raise ValueError("usage: history")
        return "\n".join(
            f"{index}  {value}"
            for index, value in enumerate(self.history_items, start=1)
        )

    def _cmd_mv(self, args):
        if len(args) != 2:
            raise ValueError("usage: mv SOURCE DESTINATION")
        self.vfs.move(args[0], args[1], self.cwd)
        return ""

    def _cmd_vfs_save(self, args):
        if len(args) != 1:
            raise ValueError("usage: vfs-save PATH")
        self.vfs.save(args[0])
        return f"saved VFS to {args[0]}"

    def _cmd_exit(self, args):
        if args:
            raise ValueError("usage: exit")
        self.should_exit = True
        return ""
