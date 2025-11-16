import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Absolute imports
from utils.basic import String, Context, global_symbol_table, List, Number
import utils.basic as basic
import paths

class ZingoEngine:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.return_value = None

    def run_string(self, code: str):
        return self._execute(code)

    def extract_value(self, value):
        """Convert Zingo objects to native Python types."""
        if isinstance(value, Number):
            return value.value
        elif isinstance(value, String):
            return value.value
        elif isinstance(value, List):
            return [self.extract_value(elem) for elem in value.elements]
        else:
            return value  # functions or unknown types

    def find_first_list(self, result):
        """Find the first Python list inside a list-like result."""
        if isinstance(result, list):
            for item in result:
                if isinstance(item, list):
                    return item
                elif isinstance(item, List):
                    extracted = self.extract_value(item)
                    if isinstance(extracted, list):
                        return extracted
        return None

    def run_zingo(self, actions, input_one, input_two=None):
        """Run a .zingo file and return the correct final Zingo value."""

        if actions == "update_state":
            filepath = paths.UPDATE_POINTS_ZINGO
        
        if actions == "update_multiplier":
            filepath = paths.UPDATE_MULTIPLIER_ZINGO

        try:
            with open(filepath, "r") as f:
                zingo_code = f.read()

            context = Context('<bridge_test>')
            context.symbol_table = global_symbol_table
            context.symbol_table.set("input_one", String(input_one))
            context.symbol_table.set("input_two", String(input_two))

            result, error = basic.run(filepath, zingo_code, context)

            if error:
                raise RuntimeError(error.as_string())

            # Convert Zingo → Python (recursive)
            result = self.extract_value(result)

            # If it's a simple value, return it directly
            if not isinstance(result, list):
                return result

            # If Zingo returned multiple top-level items (function defs etc.)
            # → extract LAST non-function item
            for item in reversed(result):
                if not callable(item):      # ignore functions
                    return item            # return the last real Zingo value

            # fallback
            return result

        except FileNotFoundError:
            raise ValueError(f"Zingo file not found: {filepath}")

if __name__ == "__main__":
    engine = ZingoEngine()
