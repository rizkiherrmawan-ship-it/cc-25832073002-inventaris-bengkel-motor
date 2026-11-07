import os
import sqlite3
import secrets
from contextlib import contextmanager
from functools import wraps
from flask import (Flask, request, redirect, url_for, session,
                   render_template_string, abort)
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "data.db")

app = Flask(__name__)
with open(os.path.join(BASE, "secret.key")) as f:
    app.secret_key = f.read().strip()
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")


@contextmanager
def db():
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS bengkel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bengkel_id INTEGER NOT NULL REFERENCES bengkel(id) ON DELETE CASCADE,
            nama TEXT NOT NULL,
            kategori TEXT,
            stok INTEGER NOT NULL DEFAULT 0,
            harga INTEGER NOT NULL DEFAULT 0)""")
        c.execute("CREATE INDEX IF NOT EXISTS idx_barang_b ON barang(bengkel_id)")


def ke_int(v):
    try:
        return max(0, int(v))
    except (TypeError, ValueError):
        return 0


HEAD = """<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Inventaris Bengkel</title>
<style>
body{font-family:Arial,sans-serif;max-width:950px;margin:20px auto;padding:0 12px}
input{padding:6px;margin:2px;max-width:100%}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ccc;padding:4px;text-align:left}
.bar{display:flex;justify-content:space-between;align-items:center}
.err{color:#b00}
</style></head><body>
{% if session.bid %}
<div class="bar"><b>{{ session.nama }}</b>
<form method="post" action="/logout"><input type="hidden" name="_t" value="{{ t }}">
<button>Keluar</button></form></div>
{% endif %}
"""
FOOT = "</body></html>"

FORM_LOGIN = """
<h2>Masuk</h2>
{% if err %}<p class="err">{{ err }}</p>{% endif %}
<form method="post"><input type="hidden" name="_t" value="{{ t }}">
<input name="email" type="email" placeholder="Email" required><br>
<input name="password" type="password" placeholder="Password" required><br>
<button>Masuk</button></form>
<p>Belum punya akun? <a href="/daftar">Daftarkan bengkel</a></p>
"""

FORM_DAFTAR = """
<h2>Daftarkan Bengkel</h2>
{% if err %}<p class="err">{{ err }}</p>{% endif %}
<form method="post"><input type="hidden" name="_t" value="{{ t }}">
<input name="nama" placeholder="Nama bengkel" required><br>
<input name="email" type="email" placeholder="Email" required><br>
<input name="password" type="password" placeholder="Password (min. 8 karakter)" required><br>
<button>Daftar</button></form>
<p>Sudah punya akun? <a href="/login">Masuk</a></p>
"""

BODY_INDEX = """
<h1>Inventaris {{ session.nama }}</h1>
<form method="post" action="/tambah"><input type="hidden" name="_t" value="{{ t }}">
<input name="nama" placeholder="Nama barang" required>
<input name="kategori" placeholder="Kategori">
<input name="stok" type="number" min="0" placeholder="Stok" required>
<input name="harga" type="number" min="0" placeholder="Harga (Rp)" required>
<button>Tambah</button></form>
<form method="get"><input name="q" value="{{ q }}" placeholder="Cari barang...">
<button>Cari</button></form>
<table>
<tr><th>Nama</th><th>Kategori</th><th>Stok</th><th>Harga</th><th>Aksi</th></tr>
{% for b in barang %}
<tr>
<td><input form="f{{ b.id }}" name="nama" value="{{ b.nama }}" required></td>
<td><input form="f{{ b.id }}" name="kategori" value="{{ b.kategori or '' }}"></td>
<td><input form="f{{ b.id }}" name="stok" type="number" min="0" value="{{ b.stok }}"></td>
<td><input form="f{{ b.id }}" name="harga" type="number" min="0" value="{{ b.harga }}"></td>
<td><form id="f{{ b.id }}" method="post" action="/ubah/{{ b.id }}">
<input type="hidden" name="_t" value="{{ t }}">
<button>Simpan</button>
<button formaction="/hapus/{{ b.id }}" onclick="return confirm('Hapus barang ini?')">Hapus</button>
</form></td>
</tr>
{% else %}
<tr><td colspan="5">Belum ada barang.</td></tr>
{% endfor %}
</table>
"""


def page(body, **ctx):
    return render_template_string(HEAD + body + FOOT, **ctx)


@app.context_processor
def inject_token():
    if "_t" not in session:
        session["_t"] = secrets.token_hex(16)
    return {"t": session["_t"]}


@app.before_request
def cek_csrf():
    if request.method == "POST":
        if not request.form.get("_t") or request.form.get("_t") != session.get("_t"):
            abort(400)


def login_required(f):
    @wraps(f)
    def wrapper(*a, **k):
        if "bid" not in session:
            return redirect(url_for("login"))
        return f(*a, **k)
    return wrapper



@app.get("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    err = ""
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip().lower()
        pw = request.form.get("password", "")
        if not nama or "@" not in email or len(pw) < 8:
            err = "Isi semua kolom. Password minimal 8 karakter."
        else:
            try:
                with db() as c:
                    cur = c.execute(
                        "INSERT INTO bengkel (nama, email, password) VALUES (?, ?, ?)",
                        (nama, email, generate_password_hash(pw)))
                    bid = cur.lastrowid
                session.clear()
                session["bid"] = bid
                session["nama"] = nama
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                err = "Email sudah terdaftar."
    return page(FORM_DAFTAR, err=err)


@app.route("/login", methods=["GET", "POST"])
def login():
    err = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pw = request.form.get("password", "")
        with db() as c:
            u = c.execute("SELECT * FROM bengkel WHERE email=?", (email,)).fetchone()
        if u and check_password_hash(u["password"], pw):
            session.clear()
            session["bid"] = u["id"]
            session["nama"] = u["nama"]
            return redirect(url_for("index"))
        err = "Email atau password salah."
    return page(FORM_LOGIN, err=err)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    with db() as c:
        if q:
            like = "%" + q + "%"
            rows = c.execute(
                "SELECT * FROM barang WHERE bengkel_id=? AND (nama LIKE ? OR kategori LIKE ?) ORDER BY nama",
                (session["bid"], like, like)).fetchall()
        else:
            rows = c.execute(
                "SELECT * FROM barang WHERE bengkel_id=? ORDER BY nama",
                (session["bid"],)).fetchall()
    return page(BODY_INDEX, barang=rows, q=q)


@app.route("/tambah", methods=["POST"])
@login_required
def tambah():
    with db() as c:
        c.execute(
            "INSERT INTO barang (bengkel_id, nama, kategori, stok, harga) VALUES (?, ?, ?, ?, ?)",
            (session["bid"], request.form["nama"].strip(), request.form.get("kategori", "").strip(),
             ke_int(request.form.get("stok")), ke_int(request.form.get("harga"))))
    return redirect(url_for("index"))


@app.route("/ubah/<int:id>", methods=["POST"])
@login_required
def ubah(id):
    with db() as c:
        c.execute(
            "UPDATE barang SET nama=?, kategori=?, stok=?, harga=? WHERE id=? AND bengkel_id=?",
            (request.form["nama"].strip(), request.form.get("kategori", "").strip(),
             ke_int(request.form.get("stok")), ke_int(request.form.get("harga")),
             id, session["bid"]))
    return redirect(url_for("index"))


@app.route("/hapus/<int:id>", methods=["POST"])
@login_required
def hapus(id):
    with db() as c:
        c.execute("DELETE FROM barang WHERE id=? AND bengkel_id=?", (id, session["bid"]))
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

