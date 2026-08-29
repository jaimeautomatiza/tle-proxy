import json
import os
import urllib.request
from datetime import datetime, timezone

ROVERS = {
    "perseverance": "https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json",
    "curiosity":    "https://mars.nasa.gov/mmgis-maps/MSL/Layers/json/MSL_waypoints.json",
}

DATA_DIR = "data"

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "SatFleetLive-RoverProxy/1.0 (https://satfleetlive.com)"
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)

def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    for rover_id, url in ROVERS.items():
        path = os.path.join(DATA_DIR, f"{rover_id}-trail.json")
        try:
            data = fetch_json(url)
            features = data.get("features", [])
            points = []
            for f in features:
                props = f.get("properties", {})
                lat = props.get("lat")
                lon = props.get("lon")
                if lat is None or lon is None:
                    continue
                dist_total_m = props.get("dist_total_m")
                points.append({
                    "lat": lat,
                    "lng": lon,
                    "sol": props.get("sol"),
                    "distTotalKm": round(dist_total_m / 1000, 2) if dist_total_m else None
                })

            with open(path, "w") as out:
                json.dump({
                    "points": points,
                    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                }, out)

            print(f"✅ {rover_id}: {len(points)} puntos guardados (histórico completo, directo de la NASA).")

        except Exception as e:
            print(f"❌ {rover_id}: fallo al consultar la NASA — {e}. Se mantiene el archivo anterior, sin tocar nada.")

if __name__ == "__main__":
    main()