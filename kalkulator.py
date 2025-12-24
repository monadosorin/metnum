import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime


# ===================== UPDATED LOGIC (INCLUDING YOUR NEW FUNCTIONS) =====================

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


# ===================== VALIDATORS (UPDATED) =====================

# SYNTAX CHECKER
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

    # tidak boleh spasi saja
    if not r:
        return False

    # tidak boleh diakhiri operator
    if r[-1] in operators:
        return False

    for i in range(len(r) - 1):
        a = r[i]
        b = r[i + 1]

        if a in operators and b in operators:
            # izinkan unary minus
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


# ===================== UI =====================

class EnhancedDiffUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Numerical Differentiation Calculator")
        self.geometry("950x750")

        #minimum window size
        self.minsize(900, 700)

        #style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        #warna
        self.bg_color = "#f8fafc"
        self.card_bg = "#ffffff"
        self.accent_color = "#3b82f6"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.warning_color = "#f59e0b"
        self.table_header_bg = "#f1f5f9"

        self.configure(bg=self.bg_color)

        self.create_enhanced_widgets()
        self.configure_styles()

    def create_enhanced_widgets(self):
        title_fr# ===================== ENHANCED UI WITH SIMPLE RESULTS DISPLAY =====================

class EnhancedDiffUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Numerical Differentiation Calculator")
        self.geometry("900x750")

        # Set minimum window size
        self.minsize(850, 700)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.bg_color = "#f8fafc"
        self.card_bg = "#ffffff"
        self.accent_color = "#3b82f6"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.warning_color = "#f59e0b"
        self.table_header_bg = "#f1f5f9"

        self.configure(bg=self.bg_color)

        self.create_enhanced_widgets()
        self.configure_styles()

    def create_enhanced_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self, bg=self.accent_color, height=100)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        title = tk.Label(title_frame, text="Numerical Differentiation Calculator",
                        font=("Segoe UI", 24, "bold"),
                        bg=self.accent_color, fg="white")
        title.pack(expand=True, pady=(15, 0))

        subtitle = tk.Label(title_frame, text="Calculate derivatives using finite difference methods",
                           font=("Segoe UI", 11),
                           bg=self.accent_color, fg="#e0f2fe")
        subtitle.pack()

        # Main container
        main_container = tk.Frame(self, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=25, pady=20)

        # Input Card
        input_card = self.create_card(main_container, "Function Input")
        input_card.pack(fill="x", pady=(0, 15))

        # Function input
        func_frame = tk.Frame(input_card, bg=self.card_bg)
        func_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(func_frame, text="V(t) =", font=("Segoe UI", 12, "bold"),
                bg=self.card_bg, fg="#4b5563").pack(side="left", padx=(0, 10))

        self.rumus_entry = ttk.Entry(func_frame, font=("Courier New", 12), width=45)
        self.rumus_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.rumus_entry.insert(0, "3*t^2 + 2*t - 5")

        # Example label (without trig functions)
        example_label = tk.Label(func_frame, text="e.g.: 3*t^2 + 2*t - 5  or  e^(0.5*t) + t^3",
                               font=("Segoe UI", 10), bg=self.card_bg, fg="#6b7280")
        example_label.pack(side="left")

        # Parameters frame
        params_frame = tk.Frame(input_card, bg=self.card_bg)
        params_frame.pack(fill="x", padx=20, pady=(0, 20))

        # t value
        t_frame = tk.Frame(params_frame, bg=self.card_bg)
        t_frame.pack(side="left", padx=(0, 30))

        tk.Label(t_frame, text="t value:", font=("Segoe UI", 11),
                bg=self.card_bg, fg="#4b5563").pack(anchor="w")

        self.t_entry = ttk.Entry(t_frame, font=("Segoe UI", 11), width=18)
        self.t_entry.pack(pady=(5, 0))
        self.t_entry.insert(0, "2.0")

        # Step size
        step_frame = tk.Frame(params_frame, bg=self.card_bg)
        step_frame.pack(side="left", padx=(0, 30))

        tk.Label(step_frame, text="Step size (h):", font=("Segoe UI", 11),
                bg=self.card_bg, fg="#4b5563").pack(anchor="w")

        self.step_entry = ttk.Entry(step_frame, font=("Segoe UI", 11), width=18)
        self.step_entry.pack(pady=(5, 0))
        self.step_entry.insert(0, "0.01")

        # Calculate button
        self.calc_btn = ttk.Button(params_frame, text="Calculate Derivatives",
                                  command=self.calculate, style="Accent.TButton")
        self.calc_btn.pack(side="right", padx=(20, 0))

        # Results Card - Using simple format like the old UI
        results_card = self.create_card(main_container, "Results")
        results_card.pack(fill="x", pady=(0, 15))

        # Create a frame for results with simple layout
        results_frame = tk.Frame(results_card, bg=self.card_bg)
        results_frame.pack(fill="x", padx=20, pady=15)

        # Initialize StringVars for results
        self.forward_var = tk.StringVar()
        self.backward_var = tk.StringVar()
        self.central_var = tk.StringVar()

        # Set default values
        self.forward_var.set("---")
        self.backward_var.set("---")
        self.central_var.set("---")

        # Create labels in simple format like old UI
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

        # Table Card
        table_card = self.create_card(main_container, "Calculation Table")
        table_card.pack(fill="both", expand=True, pady=(0, 15))

        # Create table frame
        table_frame = tk.Frame(table_card, bg=self.card_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Create Treeview for table
        columns = ("method", "f_t_minus_h", "f_t", "f_t_plus_h", "result")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=3)

        # Define headings
        self.table.heading("method", text="Method")
        self.table.heading("f_t_minus_h", text="f(t-h)")
        self.table.heading("f_t", text="f(t)")
        self.table.heading("f_t_plus_h", text="f(t+h)")
        self.table.heading("result", text="Result")

        # Set column widths
        self.table.column("method", width=120, anchor="center")
        self.table.column("f_t_minus_h", width=150, anchor="center")
        self.table.column("f_t", width=150, anchor="center")
        self.table.column("f_t_plus_h", width=150, anchor="center")
        self.table.column("result", width=150, anchor="center")

        # Style the table
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.table_header_bg)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=35)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Logs Card
        logs_card = self.create_card(main_container, "Logs / Errors")
        logs_card.pack(fill="both", expand=True)

        # Log text widget with scrollbar
        log_frame = tk.Frame(logs_card, bg=self.card_bg)
        log_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_box = tk.Text(log_frame, height=8, font=("Consolas", 10),
                              bg="#f9fafb", fg="#374151", relief="flat",
                              yscrollcommand=scrollbar.set,
                              wrap="word")
        self.log_box.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.log_box.yview)

        # Status bar
        self.status_bar = tk.Label(self, text="Ready to calculate derivatives", bg="#e5e7eb",
                                 fg="#4b5563", anchor="w", font=("Segoe UI", 10))
        self.status_bar.pack(side="bottom", fill="x", padx=25, pady=(0, 5))

        # Bind Enter key to calculate
        self.bind('<Return>', lambda e: self.calculate())

    def create_card(self, parent, title):
        """Helper function to create a styled card"""
        card = tk.Frame(parent, bg=self.card_bg, relief="flat",
                       highlightbackground="#e5e7eb", highlightthickness=1)

        # Card title
        title_label = tk.Label(card, text=title, font=("Segoe UI", 13, "bold"),
                              bg=self.card_bg, fg="#1f2937")
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        return card

    def configure_styles(self):
        """Configure custom styles for widgets"""
        # Configure button styles
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

        # Configure entry styles
        self.style.configure('TEntry',
                           padding=8,
                           relief="flat",
                           fieldbackground="#f9fafb")

    def log(self, msg):
        """Simple log function matching the old UI style"""
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

        # Update status bar
        self.status_bar.config(text=msg if len(msg) < 60 else msg[:57] + "...")

    def clear_log(self):
        """Clear the log box"""
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")
        self.status_bar.config(text="Log cleared")

    def clear_table(self):
        """Clear the calculation table"""
        for item in self.table.get_children():
            self.table.delete(item)

    def calculate(self):
        """Main calculation function"""
        # Clear previous results
        self.forward_var.set("---")
        self.backward_var.set("---")
        self.central_var.set("---")
        self.clear_table()

        # Change button state during calculation
        self.calc_btn.config(state="disabled")
        self.calc_btn.config(text="Calculating...")
        self.update()

        # Get inputs
        rumus = self.rumus_entry.get().strip()
        t_str = self.t_entry.get().strip()
        step_str = self.step_entry.get().strip()

        # Clear log
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")

        # Validate inputs
        validation_passed = True

        if not rumus:
            self.log("Error: Please enter a function")
            validation_passed = False

        if not t_str:
            self.log("Error: Please enter a value for t")
            validation_passed = False

        if not step_str:
            self.log("Error: Please enter a step size")
            validation_passed = False

        if not validation_passed:
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        try:
            t = float(t_str)
        except ValueError:
            self.log(f"Error: Invalid number for t: '{t_str}'")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        try:
            step = float(step_str)
            if step <= 0:
                self.log("Error: Step size must be positive")
                self.calc_btn.config(state="normal")
                self.calc_btn.config(text="Calculate Derivatives")
                return
        except ValueError:
            self.log(f"Error: Invalid number for step size: '{step_str}'")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        # Store original formula for display
        original_rumus = rumus

        # Validation checks
        if not check_allowed_chars(rumus):
            self.log("Error: Function contains illegal characters")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        if not check_parentheses(rumus):
            self.log("Error: Parentheses mismatch")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        if not check_empty_parentheses(rumus):
            self.log("Error: Empty parentheses () not allowed")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        if not check_operator(rumus):
            self.log("Error: Operator misuse detected")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        if not check_variable_t(rumus):
            self.log("Error: Variable 't' not found in function")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        if not check_sebelah_t(rumus):
            self.log("Error: Use operators around variable t")
            # Continue with calculation as this might be acceptable

        if not check_e_usage(rumus):
            self.log("Error: Invalid usage of constant e")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")
            return

        # Convert syntax
        if "e^" in rumus:
            rumus = rumus.replace("e^", "math.exp")
        if "^" in rumus:
            rumus = rumus.replace("^", "**")

        try:
            # Get table data
            forward, backward, central, f_t, f_th, f_tmh = tabel_perhitungan(rumus, t, step)

            if None in (forward, backward, central, f_t, f_th, f_tmh):
                self.log("Error: Function evaluation failed")
                self.forward_var.set("Error")
                self.backward_var.set("Error")
                self.central_var.set("Error")
            else:
                # Update results with formatting
                self.forward_var.set(f"{forward:.8f}")
                self.backward_var.set(f"{backward:.8f}")
                self.central_var.set(f"{central:.8f}")

                # Populate table
                self.populate_table(forward, backward, central, f_t, f_th, f_tmh, step)

        except Exception as e:
            error_msg = str(e)
            self.log(f"Error: {error_msg}")
            self.forward_var.set("Error")
            self.backward_var.set("Error")
            self.central_var.set("Error")

        finally:
            # Restore button state
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivatives")

    def populate_table(self, forward, backward, central, f_t, f_th, f_tmh, step):
        """Populate the calculation table with data"""
        # Clear existing items
        self.clear_table()

        # Insert data
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
# ===================== RUN APPLICATION =====================

if __name__ == "__main__":
    app = EnhancedDiffUI()
    app.mainloop()