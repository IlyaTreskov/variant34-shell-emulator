from emulator.config import parse_args
from emulator.gui import EmulatorGUI
from emulator.shell import Shell
from emulator.startup import run_startup_script
from emulator.vfs import VirtualFileSystem


def main():
    args = parse_args()

    if args.debug_config:
        print(f"vfs={args.vfs}")
        print(f"script={args.script}")
        print(f"debug_config={args.debug_config}")

    vfs = VirtualFileSystem()
    if args.vfs:
        vfs.load(args.vfs)

    shell = Shell(vfs)
    app = EmulatorGUI(shell)

    if args.script:
        app.after(100, lambda: run_startup_script(args.script, shell, app.write_line))

    app.mainloop()


if __name__ == "__main__":
    main()
