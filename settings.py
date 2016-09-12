import os

TC_URL = os.getenv('TC_URL', False)
TC_USER = os.getenv('TC_USER', False)
TC_PASS = os.getenv('TC_PASS', False)

# Set this to only approve nodes with this string in the name.
AGENT_WHITELIST_STRING = os.getenv('AGENT_WHITELIST_STRING', False)

# Default this to 3, which is the maximum for free licenses
TC_MAX_AGENTS = os.getenv('TC_MAX_AGENTS', 3)
