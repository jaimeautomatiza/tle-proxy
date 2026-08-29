import json
import os
import urllib.request
from datetime import datetime, timezone

ROVERS = {
    "perseverance": "https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints_current.json",
    "curiosity":    "https://mars.nasa.gov/mmgis-maps/MSL/Layers/json/MSL_waypoints_current.json",
}

DATA_DIR = "data"

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "SatFleetLive-RoverProxy/1.0 (https://satfleetlive.com)"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)

def load_trail(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"points": []}

def save_trail(path, trail):
    with open(path, "w") as f:
        json.dump(trail, f, indent=2)

def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    for rover_id, url in ROVERS.items():
        path = os.path.join(DATA_DIR, f"{rover_id}-trail.json")
        trail = load_trail(path)

        try:
            data = fetch_json(url)
            features = data.get("features", [])
            if not features:
                print(f"⚠️  {rover_id}: sin features en la respuesta, se ignora esta vez.")
                continue

            props = features[0].get("properties", {})
            lat = props.get("lat")
            lng = props.get("lon")
            sol = props.get("sol")

            if lat is None or lng is None or sol is None:
                print(f"⚠️  {rover_id}: faltan campos clave, se ignora esta vez.")
                continue

            last_point = trail["points"][-1] if trail["points"] else None
            is_new = (last_point is None) or (last_point.get("sol") != sol)

            if is_new:
                dist_total_m = props.get("dist_total_m")
                trail["points"].append({
                    "lat": lat,
                    "lng": lng,
                    "sol": sol,
                    "distTotalKm": round(dist_total_m / 1000, 2) if dist_total_m else None,
                    "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                })
                save_trail(path, trail)
                print(f"✅ {rover_id}: nuevo punto añadido (sol {sol}).")
            else:
                print(f"ℹ️  {rover_id}: sin cambios (sigue en sol {sol}).")

        except Exception as e:
            print(f"❌ {rover_id}: fallo al consultar la NASA — {e}. Se mantiene el archivo tal cual.")

if __name__ == "__main__":
    main()