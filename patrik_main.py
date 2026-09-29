"""patrik_main.py - polished interactive CLI.

Original idea kept, bugs fixed:
- crashed on non-numeric input (int(input()) with no try/except)
- used recursion for re-prompting (RecursionError on spam)
- name was lowercase / included extension logic was fragile
- no EOF / KeyboardInterrupt handling, trailing bare input()
"""
import os
import sys
import time
from datetime import datetime
import pyjokes

# --- tiny ANSI colors (work on Win10+, harmless elsewhere) ---
USE_COLOR = sys.stdout.isatty()
def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

BOLD = lambda s: _c("1", s)
GREEN = lambda s: _c("32", s)
CYAN = lambda s: _c("36", s)
YELLOW = lambda s: _c("33", s)
RED = lambda s: _c("31", s)
DIM = lambda s: _c("2", s)


def get_display_name() -> str:
    """Extract a nice display name from this filename.

    'patrik_main.py' -> 'Patrik'. Falls back to 'Friend' if unknown.
    """
    base = os.path.basename(__file__)          # patrik_main.py
    stem, _ = os.path.splitext(base)           # patrik_main
    for sep in ("_", "-", " "):
        if sep in stem:
            stem = stem.split(sep)[0]
            break
    name = stem.strip().capitalize()
    return name if name else "Friend"


def get_file_info() -> dict:
    path = os.path.abspath(__file__)
    try:
        st = os.stat(path)
        size = st.st_size
        modified = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    except OSError:
        size, modified = -1, "unknown"
    return {"path": path, "name": os.path.basename(path), "size": size, "modified": modified}


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    try:
        input(DIM("\nPress Enter to continue..."))
    except (EOFError, KeyboardInterrupt):
        print()
        raise KeyboardInterrupt


def print_banner(name: str) -> None:
    bar = "=" * 44
    print(CYAN(bar))
    print(BOLD(f"  Aha! Your name is {GREEN(name)}  "))
    print(DIM("  Welcome to the polished Patrik CLI"))
    print(CYAN(bar))


def print_menu() -> None:
    print(f"""
{BOLD('What do you want to do?')}
  {CYAN('1')} - Repeat my filename 10x (classic)
  {CYAN('2')} - Say goodbye / exit (classic)
  {CYAN('3')} - Shout my name
  {CYAN('4')} - Whisper my name backwards
  {CYAN('5')} - Name stats (length, vowels, ...)
  {CYAN('6')} - Show file info
  {CYAN('7')} - Tell me a joke
  {CYAN('8')} - Clear the screen
  {CYAN('0')} - Exit too {DIM('(also: q / quit / exit / Ctrl+C)')}
  {DIM('Tip: type h or help to show this menu again')}
""")


def action_repeat_filename(times_invalid: int) -> None:
    fname = os.path.basename(__file__)
    print(YELLOW(f"\n--- {fname} x10 ---"))
    for _ in range(10):
        print(fname)
        time.sleep(0.05)


def action_shout(name: str) -> None:
    print(GREEN(f"\n>>> {name.upper()}!!! <<<\n"))


def action_reverse(name: str) -> None:
    print(CYAN(f"\n...{name[::-1].lower()}... (psst, that's {name} backwards)\n"))


def action_stats(name: str) -> None:
    vowels = sum(1 for ch in name.lower() if ch in "aeiouy")
    print(f"""
{BOLD('Name stats:')}
  Name:          {name}
  Length:        {len(name)}
  Vowels:        {vowels}
  Consonants:    {len(name) - vowels}
  Uppercase:     {name.upper()}
  Lowercase:     {name.lower()}
""")


def action_file_info() -> None:
    info = get_file_info()
    print(f"""
{BOLD('File info:')}
  Filename:  {info['name']}
  Path:      {info['path']}
  Size:      {info['size']} bytes
  Modified:  {info['modified']}
""")


def action_joke() -> None:
    import random
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break... now it won't stop sending me KitKats.",
        "Why did the function break up with the loop? It needed space to return.",
        "There are 10 kinds of people: those who understand binary and those who don't.",
        "Debugging: being the detective in a crime movie where you are also the murderer.",
    ]
    print(YELLOW("\n" + pyjokes.get_joke() + "\n"))


def read_choice() -> str:
    """Robust prompt - never crashes on empty / non-numeric input."""
    try:
        return input(BOLD("Choose [0-8]: ")).strip()
    except EOFError:
        return "0"
    except KeyboardInterrupt:
        print()
        return "0"


def choose() -> None:
    name = get_display_name()
    invalid_attempts = 0
    actions_taken = 0

    clear_screen()
    print_banner(name)
    print_menu()

    while True:
        choice = read_choice()

        if choice in ("0", "2", "q", "quit", "exit"):
            # classic option 2 was "exit" - keep it as an alias
            if invalid_attempts > 1:
                print(RED(f"\nIT TOOK YOU {invalid_attempts} INVALID ATTEMPT(S) TO CLOSE THIS???"))
            print(GREEN(f"\nCya {name} D:  (you did {actions_taken} thing(s), {invalid_attempts} oopsie(s))"))
            break
        elif choice == "1":
            action_repeat_filename(invalid_attempts)
        elif choice == "3":
            action_shout(name)
        elif choice == "4":
            action_reverse(name)
        elif choice == "5":
            action_stats(name)
        elif choice == "6":
            action_file_info()
        elif choice == "7":
            action_joke()
        elif choice == "8":
            clear_screen()
            print_banner(name)
            print_menu()
            continue
        elif choice in ("c", "clear"):
            clear_screen()
            print_banner(name)
            print_menu()
            continue
        elif choice in ("h", "help", "?"):
            print_menu()
            continue
        elif choice == "":
            print(RED("You didn't type anything - try again ;-;"))
            invalid_attempts += 1
            continue
        else:
            invalid_attempts += 1
            print(RED(f"'{choice}' isn't an option - try 0-8. (oopsie #{invalid_attempts}) ;-;"))
            continue

        actions_taken += 1
        try:
            pause()
        except KeyboardInterrupt:
            print(GREEN(f"\nCya {name} D:"))
            break
        print_menu()


def main() -> None:
    try:
        choose()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")


if __name__ == "__main__":
    main()
    input()
