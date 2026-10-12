"""Графический эмулятор командной строки. Python 3 + Tkinter."""
import argparse
import getpass
import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from shell import Shell
from vfs import VFS


def main():
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки')
    parser.add_argument('--vfs', help='XML-файл виртуальной файловой системы')
    parser.add_argument('--script', help='Текстовый файл со стартовыми командами')
    parser.add_argument('--debug-config', action='store_true')
    args = parser.parse_args()
    if args.debug_config:
        print('vfs =', args.vfs)
        print('script =', args.script)
    try:
        shell = Shell(VFS(args.vfs))
    except (OSError, ValueError) as error:
        parser.exit(1, 'Ошибка загрузки VFS: ' + str(error) + '\n')

    window = tk.Tk()
    window.title(f'Эмулятор - [{getpass.getuser()}@{socket.gethostname()}]')
    window.geometry('680x430')
    output = ScrolledText(window, state='disabled', font=('Consolas', 11))
    output.pack(fill='both', expand=True, padx=8, pady=8)
    entry = tk.Entry(window, font=('Consolas', 11))
    entry.pack(fill='x', padx=8, pady=(0, 8))
    entry.focus_set()

    def print_text(text):
        output.configure(state='normal')
        output.insert('end', text + '\n')
        output.see('end')
        output.configure(state='disabled')

    def run_command(line):
        print_text('$ ' + line)
        try:
            result = shell.execute(line)
            if result == '__EXIT__':
                window.destroy()
                return False
            if result:
                print_text(result)
            return True
        except (ValueError, OSError) as error:
            print_text('error: ' + str(error))
            return False

    def on_enter(event=None):
        line = entry.get()
        entry.delete(0, 'end')
        run_command(line)

    entry.bind('<Return>', on_enter)
    if args.script:
        try:
            with open(args.script, encoding='utf-8') as file:
                for number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if not run_command(line):
                        print_text('script stopped at line ' + str(number))
                        break
        except (OSError, UnicodeError) as error:
            print_text('script error: ' + str(error))
    window.mainloop()


if __name__ == '__main__':
    main()
