from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from app.routers import users, jobs, mentorship
import os
import pathlib
from app.routers import users, jobs, mentorship


app = FastAPI(title="LinkNITT Backend (with static frontend)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.redirect_slashes = True
app.router.redirect_slashes = True


# include API routers
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(mentorship.router)

# mount static folder under /static
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# serve index.html on root
INDEX_FILE = STATIC_DIR / "index.html"
@app.get("/", response_class=FileResponse)
def read_index():
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return PlainTextResponse("Static frontend not found. Place files in ./static/")

# fallback for other routes to serve SPA (optional)
@app.get("/{full_path:path}", response_class=FileResponse)
def spa_fallback(full_path: str):
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return PlainTextResponse("Not found", status_code=404)

# optional: seed endpoint — this calls your seed_db.py logic
@app.post("/seed")
def seed_now():
    seed_path = BASE_DIR / "seed_db.py"
    if seed_path.exists():
        # import and run seed functions. (importing executing)
        import importlib.util
        spec = importlib.util.spec_from_file_location("seed_db", str(seed_path))
        seed_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seed_mod)
        # seed_mod should run seeds in __main__, but to be explicit:
        try:
            seed_mod.seed_users()
            seed_mod.seed_jobs()
            seed_mod.seed_mentorship()
            return PlainTextResponse("Seed executed", status_code=200)
        except Exception as e:
            return PlainTextResponse(f"Seed failed: {e}", status_code=500)
    else:
        return PlainTextResponse("seed_db.py not found", status_code=404)
