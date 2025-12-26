import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime
import sys
import io


# ===================== MAIN LOGIC =====================

def foward(rumus, t, step):
    # Hitung f(t) dan f(t+h)
    f1 = safe_eval(rumus, t)
    f2 = safe_eval(rumus, t + step)

    if f1 is None or f2 is None:
        return None

    return (f2 - f1) / step


def backward(rumus, t, step):
    # Hitung f(t) dan f(t-h)
    f1 = safe_eval(rumus, t)
    f2 = safe_eval(rumus, t - step)

    if f1 is None or f2 is None:
        return None

    return (f1 - f2) / step


def central(rumus, t, step):
    # Hitung f(t+h) dan f(t-h)
    f1 = safe_eval(rumus, t + step)
    f2 = safe_eval(rumus, t - step)

    if f1 is None or f2 is None:
        return None

    return (f1 - f2) / (2 * step)


def safe_eval(rumus, t):
    try:
        return eval(rumus, {"math": math, "e": math.e}, {"t": t})
    except ZeroDivisionError:
        return None
    except Exception:
        return None


# ===================== VALIDATORS =====================

def check_allowed_chars(rumus):
    allowed = "0123456789+-*/^.()t e"
    for c in rumus:
        if c not in allowed:
            return False
    return True


def check_parentheses(rumus):
    stack = 0
    for c in rumus:
        if c == "(":
            stack += 1
        elif c == ")":
            stack -= 1
            if stack < 0:
                return False
    return stack == 0


def check_empty_parentheses(rumus):
    return "()" not in rumus.replace(" ", "")


def check_operator(rumus):
    r = rumus.replace(" ", "")
    operators = "+-*/^"

    if not r:
        return False

    if r[-1] in operators:
        return False

    for i in range(len(r) - 1):
        a = r[i]
        b = r[i + 1]

        if a in operators and b in operators:
            if b == "-" and a in "+-*/^(":
                continue
            return False

    return True


def check_variable_t(rumus):
    return "t" in rumus


def check_sebelah_t(rumus):
    r = rumus.replace(" ", "")
    operators = "+-*/^"
    n = len(r)

    for i in range(n):
        if r[i] == "t":
            if i > 0:
                kiri = r[i - 1]
                if kiri.isdigit() or kiri == ")" or kiri == "e":
                    return False
            if i < n - 1:
                kanan = r[i + 1]
                if kanan.isdigit() or kanan == "(" or kanan == "e":
                    return False
    return True


def check_e_usage(rumus):
    r = rumus.replace(" ", "")
    operators = "+-*/^"
    n = len(r)

    for i in range(n):
        if r[i] == "e":
            if i > 0:
                kiri = r[i - 1]
                if kiri.isdigit() or kiri == ")" or kiri == "t" or kiri == "e":
                    return False
            if i < n - 1:
                kanan = r[i + 1]
                if kanan == "^":
                    continue
                if kanan.isdigit() or kanan == "t" or kanan == "e":
                    return False
    return True


def tabel_perhitungan(rumus, t, step):
    f_t = safe_eval(rumus, t)
    f_th = safe_eval(rumus, t + step)
    f_tmh = safe_eval(rumus, t - step)

    if None in (f_t, f_th, f_tmh):
        return None, None, None, f_t, f_th, f_tmh

    forward = (f_th - f_t) / step
    backward = (f_t - f_tmh) / step
    central = (f_th - f_tmh) / (2 * step)

    return forward, backward, central, f_t, f_th, f_tmh


# ===================== CONSOLE LOG =====================

class ConsoleLogger:
    def __init__(self):
        self.console_output = ""
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.buffer = io.StringIO()

    def start_logging(self):
        """Mulai menangkap output console"""
        sys.stdout = self
        sys.stderr = self

    def stop_logging(self):
        """Berhenti menangkap output console"""
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def write(self, text):
        """Tulis ke console dan buffer"""
        self.console_output += text
        self.buffer.write(text)
        self.old_stdout.write(text)  # Tetap tampilkan di console asli

    def flush(self):
        """Flush buffer"""
        self.buffer.flush()
        self.old_stdout.flush()

    def get_logs(self):
        """Ambil log yang sudah ditangkap"""
        return self.console_output

    def clear_logs(self):
        """Hapus log yang sudah ditangkap"""
        self.console_output = ""
        self.buffer = io.StringIO()


# ===================== UI =====================

class EnhancedDiffUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Diferensiasi Numerik")
        self.geometry("1000x850")  # besaran panel console

        # ukuran minimum window
        self.minsize(950, 800)

        # style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # colorssss
        self.bg_color = "#f8fafc"
        self.card_bg = "#ffffff"
        self.accent_color = "#3b82f6"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.warning_color = "#f59e0b"
        self.table_header_bg = "#f1f5f9"
        self.console_bg = "#1e1e1e"
        self.console_fg = "#d4d4d4"

        self.configure(bg=self.bg_color)


        self.console_logger = ConsoleLogger()
        self.console_logger.start_logging()

        self.create_enhanced_widgets()
        self.configure_styles()


        self.log_to_ui("=" * 60)
        self.log_to_ui("Kalkulator Diferensiasi Numerik Dimulai")
        self.log_to_ui(f"Waktu Mulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_to_ui("Siap untuk menghitung turunan numerik")
        self.log_to_ui("=" * 60)


        print("=" * 60)
        print("Numerical Differentiation Calculator Started")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    def create_enhanced_widgets(self):

        title_frame = tk.Frame(self, bg=self.accent_color, height=100)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        title = tk.Label(title_frame, text="Kalkulator Diferensiasi Numerik",
                         font=("Segoe UI", 24, "bold"),
                         bg=self.accent_color, fg="white")
        title.pack(expand=True, pady=(15, 0))

        subtitle = tk.Label(title_frame, text="Hitung turunan menggunakan metode beda hingga",
                            font=("Segoe UI", 11),
                            bg=self.accent_color, fg="#e0f2fe")
        subtitle.pack()



        container = tk.Frame(self, bg=self.bg_color)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)


        main_container = tk.Frame(canvas, bg=self.bg_color)
        canvas.create_window((0, 0), window=main_container, anchor="nw")
        window_id = canvas.create_window((0, 0), window=main_container, anchor="nw")

        def on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)


        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        main_container.bind("<Configure>", on_frame_configure)


        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


        input_card = self.create_card(main_container, "Input Fungsi")
        input_card.pack(fill="x", pady=(0, 15))


        func_frame = tk.Frame(input_card, bg=self.card_bg)
        func_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(func_frame, text="V(t) =", font=("Segoe UI", 12, "bold"),
                 bg=self.card_bg, fg="#4b5563").pack(side="left", padx=(0, 10))

        self.rumus_entry = ttk.Entry(func_frame, font=("Courier New", 12), width=45)
        self.rumus_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.rumus_entry.insert(0, "3*t^2 + 2*t - 5")


        example_label = tk.Label(func_frame, text="contoh: 3*t^2 + 2*t - 5  atau  e^(0.5*t) + t^3",
                                 font=("Segoe UI", 10), bg=self.card_bg, fg="#6b7280")
        example_label.pack(side="left")


        params_frame = tk.Frame(input_card, bg=self.card_bg)
        params_frame.pack(fill="x", padx=20, pady=(0, 20))


        t_frame = tk.Frame(params_frame, bg=self.card_bg)
        t_frame.pack(side="left", padx=(0, 30))

        tk.Label(t_frame, text="Nilai t:", font=("Segoe UI", 11),
                 bg=self.card_bg, fg="#4b5563").pack(anchor="w")

        self.t_entry = ttk.Entry(t_frame, font=("Segoe UI", 11), width=18)
        self.t_entry.pack(pady=(5, 0))
        self.t_entry.insert(0, "2.0")


        step_frame = tk.Frame(params_frame, bg=self.card_bg)
        step_frame.pack(side="left", padx=(0, 30))

        tk.Label(step_frame, text="Ukuran langkah (h):", font=("Segoe UI", 11),
                 bg=self.card_bg, fg="#4b5563").pack(anchor="w")

        self.step_entry = ttk.Entry(step_frame, font=("Segoe UI", 11), width=18)
        self.step_entry.pack(pady=(5, 0))
        self.step_entry.insert(0, "0.01")


        self.calc_btn = ttk.Button(params_frame, text="Hitung Turunan",
                                   command=self.calculate, style="Accent.TButton")
        self.calc_btn.pack(side="right", padx=(20, 0))


        results_card = self.create_card(main_container, "Hasil")
        results_card.pack(fill="x", pady=(0, 15))


        results_frame = tk.Frame(results_card, bg=self.card_bg)
        results_frame.pack(fill="x", padx=20, pady=15)


        self.forward_var = tk.StringVar()
        self.backward_var = tk.StringVar()
        self.central_var = tk.StringVar()

        self.forward_var.set("---")
        self.backward_var.set("---")
        self.central_var.set("---")


        ttk.Label(results_frame, text="Forward  :",
                  font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
        ttk.Label(results_frame, textvariable=self.forward_var,
                  font=("Segoe UI", 11)).grid(row=0, column=1, sticky="w", pady=5)

        ttk.Label(results_frame, text="Backward :",
                  font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        ttk.Label(results_frame, textvariable=self.backward_var,
                  font=("Segoe UI", 11)).grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(results_frame, text="Central  :",
                  font=("Segoe UI", 11)).grid(row=2, column=0, sticky="e", padx=(0, 10), pady=5)
        ttk.Label(results_frame, textvariable=self.central_var,
                  font=("Segoe UI", 11)).grid(row=2, column=1, sticky="w", pady=5)


        table_card = self.create_card(main_container, "Tabel Perhitungan")
        table_card.pack(fill="both", expand=True, pady=(0, 15))


        table_frame = tk.Frame(table_card, bg=self.card_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))


        columns = ("method", "f_t_minus_h", "f_t", "f_t_plus_h", "result")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=3)


        self.table.heading("method", text="Metode")
        self.table.heading("f_t_minus_h", text="f(t-h)")
        self.table.heading("f_t", text="f(t)")
        self.table.heading("f_t_plus_h", text="f(t+h)")
        self.table.heading("result", text="Hasil")


        self.table.column("method", width=120, anchor="center")
        self.table.column("f_t_minus_h", width=150, anchor="center")
        self.table.column("f_t", width=150, anchor="center")
        self.table.column("f_t_plus_h", width=150, anchor="center")
        self.table.column("result", width=150, anchor="center")


        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.table_header_bg)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=35)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        console_card = self.create_card(main_container, "Log Console")
        console_card.pack(fill="both", expand=True, pady=(0, 15))


        controls_frame = tk.Frame(console_card, bg=self.card_bg)
        controls_frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(controls_frame, text="Log Perhitungan:", font=("Segoe UI", 10, "bold"),
                 bg=self.card_bg, fg="#4b5563").pack(side="left")

        ttk.Button(controls_frame, text="Hapus Log",
                   command=self.clear_console, style="Secondary.TButton").pack(side="right", padx=(5, 0))

        ttk.Button(controls_frame, text="Salin Log",
                   command=self.copy_console_logs, style="Secondary.TButton").pack(side="right", padx=(5, 0))

        ttk.Button(controls_frame, text="Segarkan",
                   command=self.refresh_console, style="Secondary.TButton").pack(side="right", padx=(5, 0))


        console_frame = tk.Frame(console_card, bg=self.card_bg)
        console_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))


        v_scrollbar = ttk.Scrollbar(console_frame)
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = ttk.Scrollbar(console_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        self.console_box = tk.Text(console_frame, height=8, font=("Consolas", 10),
                                   bg="#f9fafb", fg="#374151",
                                   relief="flat", wrap="word",
                                   yscrollcommand=v_scrollbar.set,
                                   xscrollcommand=h_scrollbar.set)
        self.console_box.pack(side="left", fill="both", expand=True)

        v_scrollbar.config(command=self.console_box.yview)
        h_scrollbar.config(command=self.console_box.xview)


        self.status_bar = tk.Label(self, text="Siap menghitung turunan", bg="#e5e7eb",
                                   fg="#4b5563", anchor="w", font=("Segoe UI", 10))
        self.status_bar.pack(side="bottom", fill="x", padx=25, pady=(0, 5))


        self.bind('<Return>', lambda e: self.calculate())


        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_card(self, parent, title):
        """Helper function untuk membuat card yang sudah distyling"""
        card = tk.Frame(parent, bg=self.card_bg, relief="flat",
                        highlightbackground="#e5e7eb", highlightthickness=1)

        # Card title
        title_label = tk.Label(card, text=title, font=("Segoe UI", 13, "bold"),
                               bg=self.card_bg, fg="#1f2937")
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        return card

    def configure_styles(self):
        """Configure custom styles untuk widget"""

        self.style.configure('Accent.TButton',
                             font=('Segoe UI', 11, 'bold'),
                             padding=(20, 10),
                             background=self.accent_color,
                             foreground='white',
                             borderwidth=0)

        self.style.map('Accent.TButton',
                       background=[('active', '#2563eb'), ('pressed', '#1d4ed8')])

        self.style.configure('Secondary.TButton',
                             font=('Segoe UI', 9),
                             padding=(12, 6))


        self.style.configure('TEntry',
                             padding=8,
                             relief="flat",
                             fieldbackground="#f9fafb")

    def log_to_ui(self, msg, level="INFO"):
        """Log pesan ke UI console dengan timestamp dan level dalam Bahasa Indonesia"""
        timestamp = datetime.now().strftime("%H:%M:%S")


        level_translation = {
            "INFO": "INFO",
            "ERROR": "ERROR",
            "WARNING": "PERINGATAN",
            "SUCCESS": "SUKSES",
            "DEBUG": "DEBUG"
        }


        level_colors = {
            "INFO": "#374151",
            "ERROR": "#ef4444",
            "WARNING": "#f59e0b",
            "SUCCESS": "#10b981",
            "DEBUG": "#6b7280"
        }

        level_id = level_translation.get(level, "INFO")
        color = level_colors.get(level, "#374151")

        formatted_msg = f"[{timestamp}] [{level_id}] {msg}"


        if level == "ERROR":
            print(f"[ERROR] {msg}")
        elif level == "SUCCESS":
            print(f"[SUCCESS] {msg}")
        else:
            print(f"[{level}] {msg}")


        self.console_box.config(state="normal")
        self.console_box.insert("end", formatted_msg + "\n")


        start_index = self.console_box.index("end-2l linestart")
        end_index = self.console_box.index("end-2l lineend")


        if level not in self.console_box.tag_names():
            self.console_box.tag_config(level, foreground=color)

        self.console_box.tag_add(level, start_index, end_index)
        self.console_box.see("end")
        self.console_box.config(state="disabled")

    def refresh_console(self):
        """Segarkan tampilan console"""
        self.log_to_ui("Console disegarkan", "INFO")

    def clear_console(self):
        """Hapus console panel"""
        self.console_box.config(state="normal")
        self.console_box.delete("1.0", "end")
        self.console_box.config(state="disabled")
        self.log_to_ui("Log console dihapus", "INFO")

    def copy_console_logs(self):
        """Salin log console ke clipboard"""
        logs = self.console_box.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(logs)
        self.log_to_ui("Log console disalin ke clipboard", "SUCCESS")

    def log(self, msg):
        """Simple log function untuk GUI log box"""
        self.log_to_ui(msg, "INFO")

    def clear_table(self):
        """Hapus tabel perhitungan"""
        for item in self.table.get_children():
            self.table.delete(item)

    def calculate(self):
        """Fungsi perhitungan utama"""
        self.log_to_ui("=" * 50, "INFO")
        self.log_to_ui("Memulai perhitungan...", "INFO")

        # Hapus hasil sebelumnya
        self.forward_var.set("---")
        self.backward_var.set("---")
        self.central_var.set("---")
        self.clear_table()

        # Ubah state tombol selama perhitungan
        self.calc_btn.config(state="disabled")
        self.calc_btn.config(text="Menghitung...")
        self.update()

        # Ambil input
        rumus = self.rumus_entry.get().strip()
        t_str = self.t_entry.get().strip()
        step_str = self.step_entry.get().strip()

        self.log_to_ui(f"Fungsi input: V(t) = {rumus}", "DEBUG")
        self.log_to_ui(f"Nilai t: {t_str}", "DEBUG")
        self.log_to_ui(f"Ukuran langkah (h): {step_str}", "DEBUG")

        # Validasi input
        validation_passed = True

        if not rumus:
            self.log_to_ui("Error: Masukkan fungsi terlebih dahulu", "ERROR")
            validation_passed = False

        if not t_str:
            self.log_to_ui("Error: Masukkan nilai t terlebih dahulu", "ERROR")
            validation_passed = False

        if not step_str:
            self.log_to_ui("Error: Masukkan ukuran langkah (h) terlebih dahulu", "ERROR")
            validation_passed = False

        if not validation_passed:
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return

        try:
            t = float(t_str)
            self.log_to_ui(f"t yang diparsing = {t}", "DEBUG")
        except ValueError:
            self.log_to_ui(f"Error: Nilai t tidak valid: '{t_str}'", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return

        try:
            step = float(step_str)
            self.log_to_ui(f"h yang diparsing = {step}", "DEBUG")
            if step <= 0:
                self.log_to_ui("Error: Ukuran langkah (h) harus positif", "ERROR")
                self.calc_btn.config(state="normal")
                self.calc_btn.config(text="Hitung Turunan")
                return
        except ValueError:
            self.log_to_ui(f"Error: Ukuran langkah (h) tidak valid: '{step_str}'", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return

        # Simpan formula asli untuk display
        original_rumus = rumus

        # Validasi dengan logging detail
        self.log_to_ui("Menjalankan validasi...", "DEBUG")

        if not check_allowed_chars(rumus):
            self.log_to_ui("Error: Fungsi mengandung karakter yang tidak diizinkan", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return
        else:
            self.log_to_ui("✓ Valid: Pengecekan karakter diizinkan", "DEBUG")

        if not check_parentheses(rumus):
            self.log_to_ui("Error: Kurung tidak seimbang", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return
        else:
            self.log_to_ui("✓ Valid: Pengecekan keseimbangan kurung", "DEBUG")

        if not check_empty_parentheses(rumus):
            self.log_to_ui("Error: Kurung kosong () tidak diizinkan", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return
        else:
            self.log_to_ui("✓ Valid: Pengecekan kurung kosong", "DEBUG")

        if not check_operator(rumus):
            self.log_to_ui("Error: Kesalahan penggunaan operator", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return
        else:
            self.log_to_ui("✓ Valid: Pengecekan penggunaan operator", "DEBUG")

        if not check_variable_t(rumus):
            self.log_to_ui("Error: Variabel 't' tidak ditemukan dalam fungsi", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return
        else:
            self.log_to_ui("✓ Valid: Variabel 't' ditemukan", "DEBUG")

        if not check_sebelah_t(rumus):
            self.log_to_ui("Peringatan: Gunakan operator di sekitar variabel t", "WARNING")
            # Lanjutkan perhitungan karena ini mungkin bisa diterima

        if not check_e_usage(rumus):
            self.log_to_ui("Error: Penggunaan konstanta e tidak valid", "ERROR")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            return
        else:
            self.log_to_ui("✓ Valid: Pengecekan penggunaan konstanta e", "DEBUG")

        # Konversi sintaks
        if "e^" in rumus:
            rumus = rumus.replace("e^", "math.exp")
            self.log_to_ui(f"Mengubah 'e^' menjadi 'math.exp'", "DEBUG")
        if "^" in rumus:
            rumus = rumus.replace("^", "**")
            self.log_to_ui(f"Mengubah '^' menjadi '**'", "DEBUG")

        self.log_to_ui(f"Ekspresi akhir untuk evaluasi: {rumus}", "DEBUG")

        try:
            # Log titik evaluasi
            self.log_to_ui(f"Menghitung pada t = {t}, t+h = {t + step}, t-h = {t - step}", "DEBUG")

            # Ambil data tabel
            forward, backward, central, f_t, f_th, f_tmh = tabel_perhitungan(rumus, t, step)

            if None in (forward, backward, central, f_t, f_th, f_tmh):
                self.log_to_ui("Error: Evaluasi fungsi gagal (kemungkinan pembagian dengan nol)", "ERROR")
                self.forward_var.set("Error")
                self.backward_var.set("Error")
                self.central_var.set("Error")
            else:
                # Log evaluasi yang berhasil
                self.log_to_ui(f"f(t) = {f_t:.6f}", "SUCCESS")
                self.log_to_ui(f"f(t+h) = {f_th:.6f}", "SUCCESS")
                self.log_to_ui(f"f(t-h) = {f_tmh:.6f}", "SUCCESS")

                # Update hasil dengan formatting
                self.forward_var.set(f"{forward:.8f}")
                self.backward_var.set(f"{backward:.8f}")
                self.central_var.set(f"{central:.8f}")

                self.log_to_ui(f"Beda maju (forward): {forward:.8f}", "SUCCESS")
                self.log_to_ui(f"Beda mundur (backward): {backward:.8f}", "SUCCESS")
                self.log_to_ui(f"Beda pusat (central): {central:.8f}", "SUCCESS")

                # Isi tabel
                self.populate_table(forward, backward, central, f_t, f_th, f_tmh, step)

                self.log_to_ui("Perhitungan selesai dengan sukses!", "SUCCESS")

        except Exception as e:
            error_msg = str(e)
            self.log_to_ui(f"Error selama perhitungan: {error_msg}", "ERROR")
            import traceback
            self.log_to_ui(f"Traceback:\n{traceback.format_exc()}", "DEBUG")
            self.forward_var.set("Error")
            self.backward_var.set("Error")
            self.central_var.set("Error")

        finally:
            # Kembalikan state tombol
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Hitung Turunan")
            self.log_to_ui("=" * 50, "INFO")

    def populate_table(self, forward, backward, central, f_t, f_th, f_tmh, step):
        """Isi tabel perhitungan dengan data"""
        # Hapus item yang ada
        self.clear_table()

        # Masukkan data
        self.table.insert("", "end", values=(
            "Forward",
            "-",
            f"{f_t:.6f}",
            f"{f_th:.6f}",
            f"{forward:.6f}"
        ))

        self.table.insert("", "end", values=(
            "Backward",
            f"{f_tmh:.6f}",
            f"{f_t:.6f}",
            "-",
            f"{backward:.6f}"
        ))

        self.table.insert("", "end", values=(
            "Central",
            f"{f_tmh:.6f}",
            "-",
            f"{f_th:.6f}",
            f"{central:.6f}"
        ))

    def on_closing(self):
        """Handle event penutupan window"""
        self.log_to_ui("=" * 60, "INFO")
        self.log_to_ui("Aplikasi ditutup...", "INFO")
        self.log_to_ui(f"Waktu Selesai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        self.log_to_ui("=" * 60, "INFO")

        # Berhenti menangkap console
        self.console_logger.stop_logging()

        # Tutup window
        self.destroy()


# ===================== RUN APPLICATION =====================

if __name__ == "__main__":
    app = EnhancedDiffUI()
    app.mainloop()