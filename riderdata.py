import re
import csv

# Read your saved HTML lines
with open("riders.txt", "r", encoding="utf-8") as f:
    data = f.read()

# Find all <tr> ... </tr> blocks
rows = re.findall(r"<tr.*?</tr>", data, flags=re.DOTALL)

parsed_rows = []
for row in rows:
    # Determine if injured
    injured = 1 if 'alt="injury"' in row else 0

    # Extract rider name (text after last "flag"> and before next <img or </a>)
    name_match = re.search(r"flag\">(.*?)</a>", row)
    if name_match:
        name = name_match.group(1)
        # Remove injury icon text if it's still in the name
        name = re.sub(r"<img.*?>", "", name).strip()
    else:
        name = ""

    # Extract cost (remove $ and commas)
    cost_match = re.search(r"<td>\$(.*?)</td>", row)
    cost = int(cost_match.group(1).replace(",", "")) if cost_match else None

    # Extract points
    points_match = re.search(r"</td><td>(\d+)</td><td>", row)
    points = int(points_match.group(1)) if points_match else None

    # Extract gender (last <td> in row)
    gender_match = re.search(r"<td>(Male|Female)</td>", row)
    gender = gender_match.group(1) if gender_match else ""

    parsed_rows.append([name, cost, points, gender, injured])

# Save to CSV
with open("pinkbike_riders.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["rider", "cost", "points", "gender", "injured"])
    writer.writerows(parsed_rows)

print(f"Saved {len(parsed_rows)} riders to pinkbike_riders.csv")
