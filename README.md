# tle-proxy

Proxy de datos TLE (Two-Line Element) para SatFleet Live.

GitHub Actions fetchea los datos de CelesTrak cada 2 horas y los guarda aquí.
GitHub Pages los sirve como JSON público con CORS abierto.

## URLs públicas

```
https://jaime.automatiza.github.io/tle-proxy/data/tle.json
https://jaime.automatiza.github.io/tle-proxy/data/meta.json
```

## Setup (una sola vez)

1. Ve a **Settings → Pages** de este repo
2. Source: **Deploy from a branch**
3. Branch: **main** / Folder: **/ (root)**
4. Guarda. En 1-2 minutos tendrás la URL activa.

## Lanzar manualmente

Actions → "Fetch TLE Data" → Run workflow