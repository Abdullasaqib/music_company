import json
import datetime
import os

# Paths
DATA_PATH = os.path.join("data", "company_state.json")
DOCS_PATH = os.path.join("docs", "images")
os.makedirs(DOCS_PATH, exist_ok=True)

def load_data():
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

def create_svg(path, title, x_label, y_label, dates, values, color):
    width = 800
    height = 400
    padding = 60
    
    if not values: return

    # Normalize data
    min_val = min(values)
    max_val = max(values)
    val_range = max_val - min_val if max_val != min_val else 1
    
    points = []
    num_points = len(values)
    
    for i, val in enumerate(values):
        x = padding + (i / (num_points - 1)) * (width - 2 * padding)
        y = height - padding - ((val - min_val) / val_range) * (height - 2 * padding)
        points.append(f"{x},{y}")
    
    polyline = " ".join(points)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="background-color:#121212; font-family:sans-serif;">
    <text x="{width/2}" y="30" fill="white" font-size="20" text-anchor="middle" font-weight="bold">{title}</text>
    
    <!-- Axes -->
    <line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="white" stroke-width="2" />
    <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="white" stroke-width="2" />
    
    <!-- Labels -->
    <text x="{width/2}" y="{height-15}" fill="#888" font-size="14" text-anchor="middle">{x_label}</text>
    <text x="15" y="{height/2}" fill="#888" font-size="14" text-anchor="middle" transform="rotate(-90 15,{height/2})">{y_label}</text>
    
    <!-- Graph -->
    <polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="3" />
    <circle cx="{points[-1].split(',')[0]}" cy="{points[-1].split(',')[1]}" r="4" fill="{color}" />
    
    <!-- Max Value Tag -->
    <text x="{width-padding}" y="{padding+20}" fill="{color}" font-size="16" text-anchor="end">Max: {max_val:.2f}</text>
</svg>"""

    with open(path, 'w') as f:
        f.write(svg)
    print(f"Generated {path}")

def generate_revenue_chart(data):
    logs = data.get("billing_log", [])
    if not logs: return

    logs.sort(key=lambda x: x["timestamp"])
    revenue = []
    accumulated = 0
    dates = []

    for log in logs:
        try:
            val_str = log["message"].split("$")[1].split(" ")[0]
            val = float(val_str)
            accumulated += val
            revenue.append(accumulated)
            dates.append(log["timestamp"])
        except: continue
            
    if revenue:
        create_svg(os.path.join(DOCS_PATH, "revenue_chart.svg"), "Total Revenue Growth", "Time", "Revenue ($)", dates, revenue, "#00ff88")

def generate_catalog_chart(data):
    catalog = data.get("catalog", [])
    if not catalog: return

    catalog.sort(key=lambda x: x["timestamp"])
    counts = []
    dates = []
    
    for i, _ in enumerate(catalog):
        counts.append(i + 1)
        dates.append(catalog[i]["timestamp"])
            
    if counts:
        create_svg(os.path.join(DOCS_PATH, "catalog_chart.svg"), "Catalog Size", "Time", "Tracks", dates, counts, "#00ccff")

if __name__ == "__main__":
    data = load_data()
    generate_revenue_chart(data)
    generate_catalog_chart(data)
