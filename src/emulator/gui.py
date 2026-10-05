import getpass
import socket
import tkinter as tk


class EmulatorGUI(tk.Tk):
    def __init__(self, shell):
        super().__init__()
        self.shell = shell
        username = getpass.getuser()
        hostname = socket.gethostname()
        self.title(f"Эмулятор - [{username}@{hostname}]")
        self.geometry("760x480")

        self.output = tk.Text(self, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x", padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()
        self.write_line("Эмулятор UNIX-подобной оболочки. Введите команду.")

    def write_line(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def _on_enter(self, _event=None):
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.write_line(f"$ {line}")
        ok, message = self.shell.execute(line)
        if message:
            self.write_line(message)
        if self.shell.should_exit:
            self.destroy()
        return "break"
