# utils/zingo_engine.py
import re

class ZingoEngine:
    def __init__(self, context=None):
        self.context = context or {}

    def register(self, name, function):
        """Register a callable function exposed to Zingo."""
        self.context[name.upper()] = function

    def execute_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return

        # Match: COMMAND(arg1, arg2, ...)
        match = re.match(r"(\w+)\((.*)\)$", line)
        if not match:
            print(f"[Zingo] Syntax error: {line}")
            return

        cmd, raw_args = match.groups()
        cmd = cmd.upper()

        args = []
        if raw_args.strip():
            # Split args by commas respecting quotes
            parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', raw_args)
            args = [p.strip().strip('"').strip("'") for p in parts]

        if cmd not in self.context:
            print(f"[Zingo] Unknown command: {cmd}")
            return

        func = self.context[cmd]

        try:
            func(*args)
        except Exception as e:
            print(f"[Zingo] Error calling {cmd}: {e}")

    def execute_script(self, script):
        for line in script.splitlines():
            self.execute_line(line)

    def execute_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.execute_script(f.read())
