import sys
from pathlib import Path
# Add this day's directory to the front of sys.path
_this_day = str(Path(__file__).parent)
if _this_day not in sys.path:
    sys.path.insert(0, _this_day)
