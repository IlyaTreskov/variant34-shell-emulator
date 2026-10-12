"""Выполнение команд эмулятора."""
import shlex
from vfs import VFS


class Shell:
    def __init__(self, vfs=None):
        self.vfs = vfs or VFS()
        self.history = []

    def execute(self, line):
        if not line.strip():
            return ''
        try:
            args = shlex.split(line)
        except ValueError as error:
            raise ValueError('parse error: ' + str(error))
        if not args:
            return ''
        self.history.append(line)
        command = args[0]
        params = args[1:]
        if command == 'ls' and len(params) <= 1:
            return self.vfs.ls(params[0] if params else '.')
        if command == 'cd' and len(params) <= 1:
            self.vfs.cd(params[0] if params else '/')
            return ''
        if command == 'tac' and len(params) == 1:
            return '\n'.join(reversed(self.vfs.read(params[0]).splitlines()))
        if command == 'head':
            if len(params) == 1:
                count, filename = 10, params[0]
            elif len(params) == 3 and params[0] == '-n':
                try:
                    count = int(params[1])
                except ValueError:
                    raise ValueError('head: N must be an integer')
                filename = params[2]
            else:
                raise ValueError('usage: head [-n N] FILE')
            if count < 0:
                raise ValueError('head: N must be nonnegative')
            return '\n'.join(self.vfs.read(filename).splitlines()[:count])
        if command == 'history' and not params:
            return '\n'.join(f'{i}  {cmd}' for i, cmd in enumerate(self.history, 1))
        if command == 'mv' and len(params) == 2:
            self.vfs.mv(params[0], params[1])
            return ''
        if command == 'vfs-save' and len(params) == 1:
            self.vfs.save(params[0])
            return 'saved VFS to ' + params[0]
        if command == 'exit' and not params:
            return '__EXIT__'
        if command in ('ls', 'cd', 'tac', 'head', 'history', 'mv', 'vfs-save', 'exit'):
            raise ValueError('wrong arguments for ' + command)
        raise ValueError('unknown command: ' + command)
