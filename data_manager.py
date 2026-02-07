import json
import os
import tempfile
import sqlite3

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_JUGADOR     = os.path.join(_BASE_DIR, "datos_jugador.json")
PATH_VOLUMEN     = os.path.join(_BASE_DIR, "datos_volumen.json")
PATH_NIVELES     = os.path.join(_BASE_DIR, "datos_niveles.json")
PATH_NIVEL1      = os.path.join(_BASE_DIR, "datos_nivel1.json")
PATH_NIVEL2      = os.path.join(_BASE_DIR, "datos_nivel2.json")
PATH_NIVEL3      = os.path.join(_BASE_DIR, "datos_nivel3.json")
PATH_LEADERBOARD = os.path.join(_BASE_DIR, "leaderboard1.db")

DEFAULT_JUGADOR = {
    "salud": 100,
    "vida": 2,
    "puntaje": 0,
    "nivel completado": 0,
    "nivel actual": "niveles.uno",
    "muerto": 0,
    "Muertes": 0,
    "Tiempo": 3000,
    "Puntaje Nivel": 0,
}

DEFAULT_VOLUMEN = {
    "volumen_musica": 1,
    "volumen_efectos": 100,
    "bandera": True,
    "pausa": False,
}

DEFAULT_NIVELES = {
    "nivel1": 0,
    "recordlvl1": 0,
    "nivel2": 0,
    "recordlvl2": 0,
    "nivel3": 0,
    "recordlvl3": 0,
    "game_over": 0,
    "medio": 0,
    "record final": 0,
}

DEFAULT_NIVEL_DATA = {
    "salud": 100,
    "vida": 1,
    "puntaje": 0,
    "nivel completado": 0,
    "nivel actual": "",
    "muerto": 0,
    "Muertes": 0,
    "Tiempo": 3000,
    "Puntaje Nivel": 0,
}


class DataManager:
    def __init__(self):
        self.jugador = {}
        self.volumen = {}
        self.niveles = {}
        self.nivel1 = {}
        self.nivel2 = {}
        self.nivel3 = {}
        self.load_all()
        self._ensure_leaderboard_db()

    # --- Generic JSON helpers ---

    def _load_json(self, path, defaults):
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = dict(defaults)
                merged.update(data)
                return merged
        except (json.JSONDecodeError, OSError, ValueError):
            pass
        return dict(defaults)

    def _save_json(self, path, data):
        tmp_path = None
        try:
            dir_name = os.path.dirname(path)
            fd, tmp_path = tempfile.mkstemp(suffix=".tmp", dir=dir_name)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f)
            os.replace(tmp_path, path)
        except OSError as e:
            print(f"[DataManager] Error saving {path}: {e}")
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    # --- Load methods ---

    def load_all(self):
        self.load_jugador()
        self.load_volumen()
        self.load_niveles()
        self.load_nivel1()
        self.load_nivel2()
        self.load_nivel3()

    def load_jugador(self):
        self.jugador = self._load_json(PATH_JUGADOR, DEFAULT_JUGADOR)

    def load_volumen(self):
        self.volumen = self._load_json(PATH_VOLUMEN, DEFAULT_VOLUMEN)

    def load_niveles(self):
        self.niveles = self._load_json(PATH_NIVELES, DEFAULT_NIVELES)

    def load_nivel1(self):
        self.nivel1 = self._load_json(PATH_NIVEL1, DEFAULT_NIVEL_DATA)

    def load_nivel2(self):
        self.nivel2 = self._load_json(PATH_NIVEL2, DEFAULT_NIVEL_DATA)

    def load_nivel3(self):
        self.nivel3 = self._load_json(PATH_NIVEL3, DEFAULT_NIVEL_DATA)

    # --- Save methods ---

    def save_jugador(self):
        self._save_json(PATH_JUGADOR, self.jugador)

    def save_volumen(self):
        self._save_json(PATH_VOLUMEN, self.volumen)

    def save_niveles(self):
        self._save_json(PATH_NIVELES, self.niveles)

    def save_nivel1(self):
        self._save_json(PATH_NIVEL1, self.nivel1)

    def save_nivel2(self):
        self._save_json(PATH_NIVEL2, self.nivel2)

    def save_nivel3(self):
        self._save_json(PATH_NIVEL3, self.nivel3)

    def save_all(self):
        self.save_jugador()
        self.save_volumen()
        self.save_niveles()
        self.save_nivel1()
        self.save_nivel2()
        self.save_nivel3()

    # --- Reset (game over) ---

    def reset_jugador(self):
        self.jugador = dict(DEFAULT_JUGADOR)
        try:
            if os.path.isfile(PATH_JUGADOR):
                os.remove(PATH_JUGADOR)
        except OSError:
            pass

    def reset_niveles(self):
        self.niveles = dict(DEFAULT_NIVELES)
        try:
            if os.path.isfile(PATH_NIVELES):
                os.remove(PATH_NIVELES)
        except OSError:
            pass

    # --- SQLite Leaderboard ---

    def _ensure_leaderboard_db(self):
        try:
            with sqlite3.connect(PATH_LEADERBOARD) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS mi_tabla (
                        score INTEGER PRIMARY KEY,
                        nombre TEXT
                    )
                """)
        except sqlite3.Error as e:
            print(f"[DataManager] Leaderboard DB error: {e}")

    def leaderboard_seed(self, entries):
        try:
            with sqlite3.connect(PATH_LEADERBOARD) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM mi_tabla")
                if cursor.fetchone()[0] == 0:
                    conn.executemany(
                        "INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)",
                        entries,
                    )
        except sqlite3.Error as e:
            print(f"[DataManager] Leaderboard seed error: {e}")

    def leaderboard_get_top(self, limit=5):
        try:
            with sqlite3.connect(PATH_LEADERBOARD) as conn:
                cursor = conn.execute(
                    "SELECT score, nombre FROM mi_tabla ORDER BY score DESC LIMIT ?",
                    (limit,),
                )
                return [
                    {"score": row[0], "nombre": row[1]}
                    for row in cursor.fetchall()
                ]
        except sqlite3.Error as e:
            print(f"[DataManager] Leaderboard read error: {e}")
            return []

    def leaderboard_upsert(self, score, nombre):
        try:
            with sqlite3.connect(PATH_LEADERBOARD) as conn:
                cursor = conn.execute(
                    "UPDATE mi_tabla SET nombre = ? WHERE score = ?",
                    (nombre, score),
                )
                if cursor.rowcount == 0:
                    conn.execute(
                        "INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)",
                        (score, nombre),
                    )
                conn.commit()
        except sqlite3.Error as e:
            print(f"[DataManager] Leaderboard upsert error: {e}")


dm = DataManager()
