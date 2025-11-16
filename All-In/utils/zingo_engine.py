from utils.basic import String, Context, global_symbol_table
import utils.basic as basic

# utils/zingo_engine.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import paths

class ZingoEngine:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.return_value = None

    def run_string(self, code: str):
        # you already have this implemented
        return self._execute(code)

    def run_zingo(self, text, filepath: str=paths.ZINGO_FILE):
        """Read a .zingo file and run it."""
        try:
            with open(filepath, "r") as f:
                zingo_code = f.read()

            context = Context('<bridge_test>')
            context.symbol_table = global_symbol_table

            context.symbol_table.set("input_value", String(text))

            result, error = basic.run("test.zingo", zingo_code, context) 

            if error:
                return error.as_string()
            else:
                return result

        except FileNotFoundError:
            raise ValueError(f"Zingo file not found: {filepath}")


if __name__ == "__main__":
    engine = ZingoEngine()