import re

text = "User ID: f9f2a3d8-4bfb-4e5a-a4db-ed15843f1b81"
pattern = r"User ID: ([a-zA-Z0-9\-]+)"

match = re.search(pattern, text)
if match:
    user_id = match.group(2)
    print(user_id)  # Output: f9f2a3d8-4bfb-4e5a-a4db-ed15843f1b81
