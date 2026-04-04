import re

lines = [
    "- Security: 5/10 - **Corporate Standard**",
    "- Police response time: 5/10 - **Standard Urban**",
    "- Revenue: 2/10 **Small Firm**",
    "- Resources 2/10 **Basic Utility**",
    "- Players Reputations 2/10 - **Hostile**",
    "- Just numbers: 5/10"
]

for line in lines:
    m = re.match(r'-\s+(.*?)(?::)?\s+(\d+)/(\d+)(?:[\s-]+(.+))?$', line.strip())
    if m:
        print(f"MATCH: {line}")
        print(f"  1: {m.group(1)}")
        print(f"  2: {m.group(2)}")
        print(f"  3: {m.group(3)}")
        print(f"  4: {m.group(4)}")
    else:
        print(f"NO MATCH: {line}")
