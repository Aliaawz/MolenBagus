from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os # Untuk variabel lingkungan
import bcrypt # Library untuk hashing password

app = Flask(__name__)
app.secret_key = os.urandom(24) # Kunci rahasia untuk session, ganti di produksi!

# ====================================================================
# KONFIGURASI DATABASE DINAMIS BERDASARKAN LINGKUNGAN
# ====================================================================

def get_db_config():
    if os.getenv('FLASK_ENV') == 'production': # Contoh deteksi lingkungan produksi
        # Konfigurasi untuk Lingkungan ONLINE (InfinityFree, Hostinger, dll.)
        # GANTI KREDENSIAL INI DENGAN INFORMASI DARI HOSTING ONLINE KAMU!
        return {
            'host': 'sql307.infinityfree.com', # MySQL Host Name dari InfinityFree
            'user': 'ifo_39420600',           # MySQL User Name dari InfinityFree
            'password': 'YOUR_V_PANEL_PASSWORD_HERE', # <--- SANGAT PENTING: GANTI DENGAN PASSWORD V-PANEL ASLI KAMU!
            'database': 'ifo_39420600_molen_bagus' # MySQL DB Name dari InfinityFree
        }
    else:
        # Konfigurasi untuk Lingkungan LOKAL (XAMPP)
        return {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'molen_bagus_db' # Nama database lokal kamu
        }

# Fungsi untuk mendapatkan koneksi database
def get_db_connection():
    config = get_db_config()
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        # Di produksi, Anda mungkin ingin melakukan logging error ini
        return None

# ====================================================================
# ROUTING APLIKASI
# ====================================================================

# Rute Home/Indeks
@app.route('/')
def index():
    # Contoh: mengambil data produk dari database (nanti kita isi)
    products = []
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True) # Mengambil hasil sebagai dictionary
        cursor.execute("SELECT id, name, price, image, description FROM products")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('index.html', products=products) # Nanti kita integrasikan desainmu ke sini

# --- ROUTE UNTUK LOGIN & REGISTRASI AKAN DITAMBAHKAN DI SINI ---
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Logika login akan ditambahkan
#     pass

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     # Logika registrasi akan ditambahkan
#     pass

# --- ROUTE UNTUK ADMIN DASHBOARD DAN CRUD AKAN DITAMBAHKAN DI SINI ---
# @app.route('/admin/dashboard')
# def admin_dashboard():
#     # Logika dashboard admin
#     pass


# ====================================================================
# MENJALANKAN APLIKASI
# ====================================================================
if __name__ == '__main__':
    app.run(debug=True) # debug=True akan otomatis restart server saat ada perubahan kode