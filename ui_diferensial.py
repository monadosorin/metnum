import tkinter as tk
from tkinter import ttk, messagebox
import math
import io
import sys

# ===================== MAIN LOGIC =====================

def foward(rumus, t, step):
    f1 = safe_eval(rumus, t)
    f2 = safe_eval(rumus, t + step)
    return (f2 - f1) / step

def backward(rumus, t, step):
    f1 = safe_eval(rumus, t)
    f2 = safe_eval(rumus, t - step)
    return (f1 - f2) / step

def central(rumus, t, step):
    f1 = safe_eval(rumus, t + step)
    f2 = safe_eval(rumus, t - step)
    return (f1 - f2) / (2 * step)

def safe_eval(rumus, t):
    return eval(rumus, {"math": math, "e": math.e}, {"t": t})

# ===================== VALIDATORS =====================

def check_allowed_chars(r):
    return all(c in "0123456789+-*/^.()t e" for c in r)

def check_parentheses(r):
    stack = 0
    for c in r:
        if c == "(":
            stack += 1
        elif c == ")":
            stack -= 1
            if stack < 0:
                return False
    return stack == 0

def check_operator(r):
    r = r.replace(" ", "")
    ops = "+-*/^"
    if not r or r[-1] in ops:
        return False
    for i in range(len(r) - 1):
        if r[i] in ops and r[i+1] in ops:
            return False
    return True

def check_variable_t(r):
    return "t" in r

# ===================== GUI =====================

class DiffUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Numerical Differentiation Calculator")
        self.geometry("600x500")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Numerical Differentiation", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # Input Frame
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Label(frame, text="V(t) =").grid(row=0, column=0, sticky="e")
        self.rumus_entry = ttk.Entry(frame, width=40)
        self.rumus_entry.grid(row=0, column=1, columnspan=3, padx=5)

        ttk.Label(frame, text="t =").grid(row=1, column=0, sticky="e")
        self.t_entry = ttk.Entry(frame, width=10)
        self.t_entry.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="Step =").grid(row=1, column=2, sticky="e")
        self.step_entry = ttk.Entry(frame, width=10)
        self.step_entry.grid(row=1, column=3, padx=5)

        ttk.Button(self, text="Calculate", command=self.calculate).pack(pady=10)

        # Results
        result_frame = ttk.LabelFrame(self, text="Results")
        result_frame.pack(fill="x", padx=20, pady=10)

        self.forward_var = tk.StringVar()
        self.backward_var = tk.StringVar()
        self.central_var = tk.StringVar()

        ttk.Label(result_frame, text="Forward  :").grid(row=0, column=0, sticky="e")
        ttk.Label(result_frame, textvariable=self.forward_var).grid(row=0, column=1, sticky="w")

        ttk.Label(result_frame, text="Backward :").grid(row=1, column=0, sticky="e")
        ttk.Label(result_frame, textvariable=self.backward_var).grid(row=1, column=1, sticky="w")

        ttk.Label(result_frame, text="Central  :").grid(row=2, column=0, sticky="e")
        ttk.Label(result_frame, textvariable=self.central_var).grid(row=2, column=1, sticky="w")

        # Logs
        log_frame = ttk.LabelFrame(self, text="Logs / Errors")
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.log_box = tk.Text(log_frame, height=8, state="disabled")
        self.log_box.pack(fill="both", expand=True)

    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.config(state="disabled")

    def calculate(self):
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")

        rumus = self.rumus_entry.get()
        try:
            t = float(self.t_entry.get())
            step = float(self.step_entry.get())
            if step <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "t and Step must be valid numbers")
            return

        # Validation
        if not check_allowed_chars(rumus):
            self.log("Error: illegal characters")
            return
        if not check_parentheses(rumus):
            self.log("Error: parentheses mismatch")
            return
        if not check_operator(rumus):
            self.log("Error: operator misuse")
            return
        if not check_variable_t(rumus):
            self.log("Error: variable t not found")
            return

        # Convert syntax
        rumus = rumus.replace("e^", "math.exp")
        rumus = rumus.replace("^", "**")

        try:
            self.forward_var.set(foward(rumus, t, step))
            self.backward_var.set(backward(rumus, t, step))
            self.central_var.set(central(rumus, t, step))
        except Exception as e:
            self.log(str(e))


# ===================== ENHANCED UI =====================
class EnhancedDiffUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Numerical Differentiation Calculator")
        self.geometry("750x650")
        self.resizable(True, True)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.bg_color = "#f0f5ff"
        self.card_bg = "#ffffff"
        self.accent_color = "#4a6fa5"
        self.success_color = "#2e7d32"
        self.error_color = "#c62828"

        self.configure(bg=self.bg_color)

        self.create_enhanced_widgets()

    def create_enhanced_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self, bg=self.accent_color, height=80)
        title_frame.pack(fill="x", side="top")
        title_frame.pack_propagate(False)

        title = tk.Label(title_frame, text="Numerical Differentiation Calculator",
                         font=("Segoe UI", 22, "bold"),
                         bg=self.accent_color, fg="white")
        title.pack(expand=True)

        subtitle = tk.Label(title_frame, text="Calculate derivatives using finite difference methods",
                            font=("Segoe UI", 10),
                            bg=self.accent_color, fg="#e0e0e0")
        subtitle.pack()

        # Main container
        main_container = tk.Frame(self, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Input Card
        input_card = tk.Frame(main_container, bg=self.card_bg, relief="flat",
                              highlightbackground="#e0e0e0", highlightthickness=1)
        input_card.pack(fill="x", pady=(0, 15))

        tk.Label(input_card, text="Function Input", font=("Segoe UI", 12, "bold"),
                 bg=self.card_bg, fg="#333333").pack(anchor="w", padx=15, pady=(15, 5))

        # Function input
        func_frame = tk.Frame(input_card, bg=self.card_bg)
        func_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(func_frame, text="V(t) =", font=("Segoe UI", 11),
                 bg=self.card_bg, fg="#555555").pack(side="left", padx=(0, 10))

        self.rumus_entry = ttk.Entry(func_frame, font=("Courier New", 11), width=40)
        self.rumus_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Example label
        example_label = tk.Label(func_frame, text="e.g.: 3*t^2 + 2*sin(t) - e^(0.5*t)",
                                 font=("Segoe UI", 9), bg=self.card_bg, fg="#777777")
        example_label.pack(side="left")

        # Parameters frame
        params_frame = tk.Frame(input_card, bg=self.card_bg)
        params_frame.pack(fill="x", padx=15, pady=(10, 15))

        # t value
        t_frame = tk.Frame(params_frame, bg=self.card_bg)
        t_frame.pack(side="left", padx=(0, 30))

        tk.Label(t_frame, text="t value:", font=("Segoe UI", 10),
                 bg=self.card_bg, fg="#555555").pack(anchor="w")

        self.t_entry = ttk.Entry(t_frame, font=("Segoe UI", 11), width=15)
        self.t_entry.pack(pady=(5, 0))
        self.t_entry.insert(0, "1.0")

        # Step size
        step_frame = tk.Frame(params_frame, bg=self.card_bg)
        step_frame.pack(side="left", padx=(0, 30))

        tk.Label(step_frame, text="Step size (h):", font=("Segoe UI", 10),
                 bg=self.card_bg, fg="#555555").pack(anchor="w")

        self.step_entry = ttk.Entry(step_frame, font=("Segoe UI", 11), width=15)
        self.step_entry.pack(pady=(5, 0))
        self.step_entry.insert(0, "0.01")

        # Calculate button
        self.calc_btn = ttk.Button(params_frame, text="Calculate Derivative",
                                   command=self.calculate, style="Accent.TButton")
        self.calc_btn.pack(side="right", padx=(20, 0))

        # Results Card
        results_card = tk.Frame(main_container, bg=self.card_bg, relief="flat",
                                highlightbackground="#e0e0e0", highlightthickness=1)
        results_card.pack(fill="x", pady=(0, 15))

        tk.Label(results_card, text="Results", font=("Segoe UI", 12, "bold"),
                 bg=self.card_bg, fg="#333333").pack(anchor="w", padx=15, pady=(15, 10))

        # Results display
        results_grid = tk.Frame(results_card, bg=self.card_bg)
        results_grid.pack(fill="x", padx=15, pady=(0, 15))

        methods = [("Forward Difference", "#4a6fa5"),
                   ("Backward Difference", "#6a5fa5"),
                   ("Central Difference", "#4a8fa5")]

        self.result_vars = []
        self.result_labels = []

        for i, (method, color) in enumerate(methods):
            frame = tk.Frame(results_grid, bg=self.card_bg)
            frame.grid(row=i, column=0, sticky="w", pady=5)

            tk.Label(frame, text=method + ":", font=("Segoe UI", 10, "bold"),
                     bg=self.card_bg, fg=color).pack(side="left", padx=(0, 10))

            var = tk.StringVar()
            var.set("---")
            result_label = tk.Label(frame, textvariable=var, font=("Segoe UI", 11, "bold"),
                                    bg=self.card_bg, fg="#222222")
            result_label.pack(side="left")

            self.result_vars.append(var)
            self.result_labels.append(result_label)

        # Logs Card
        logs_card = tk.Frame(main_container, bg=self.card_bg, relief="flat",
                             highlightbackground="#e0e0e0", highlightthickness=1)
        logs_card.pack(fill="both", expand=True)

        header_frame = tk.Frame(logs_card, bg=self.card_bg)
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        tk.Label(header_frame, text="Calculation Log", font=("Segoe UI", 12, "bold"),
                 bg=self.card_bg, fg="#333333").pack(side="left")

        # Clear log button
        clear_btn = ttk.Button(header_frame, text="Clear Log",
                               command=self.clear_log, style="Secondary.TButton")
        clear_btn.pack(side="right")

        # Log text widget with scrollbar
        log_frame = tk.Frame(logs_card, bg=self.card_bg)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_box = tk.Text(log_frame, height=8, font=("Consolas", 10),
                               bg="#f8f9fa", fg="#333333", relief="flat",
                               yscrollcommand=scrollbar.set,
                               wrap="word")
        self.log_box.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.log_box.yview)

        # Status bar
        self.status_bar = tk.Label(self, text="Ready", bg="#e8e8e8",
                                   fg="#666666", anchor="w", font=("Segoe UI", 9))
        self.status_bar.pack(side="bottom", fill="x")

        # Configure styles
        self.configure_styles()

        # Bind Enter key to calculate
        self.bind('<Return>', lambda e: self.calculate())

    def configure_styles(self):
        # Configure button styles
        self.style.configure('Accent.TButton',
                             font=('Segoe UI', 10, 'bold'),
                             padding=10,
                             background=self.accent_color,
                             foreground='white')

        self.style.map('Accent.TButton',
                       background=[('active', '#3a5a85'), ('pressed', '#2a4a75')])

        self.style.configure('Secondary.TButton',
                             font=('Segoe UI', 9),
                             padding=6)

        # Configure entry styles
        self.style.configure('TEntry',
                             padding=8,
                             relief="flat")

    def log(self, msg, msg_type="info"):
        """Enhanced log function with message types"""
        self.log_box.config(state="normal")

        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Color coding based on message type
        if msg_type == "error":
            prefix = f"[{timestamp}] ERROR: "
            tag = "error"
            self.log_box.tag_config("error", foreground=self.error_color)
        elif msg_type == "success":
            prefix = f"[{timestamp}] SUCCESS: "
            tag = "success"
            self.log_box.tag_config("success", foreground=self.success_color)
        else:
            prefix = f"[{timestamp}] INFO: "
            tag = "info"
            self.log_box.tag_config("info", foreground="#333333")

        self.log_box.insert("end", prefix + msg + "\n", tag)
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

    def calculate(self):
        """Enhanced calculate function with better visual feedback"""
        # Clear previous results
        for var in self.result_vars:
            var.set("---")

        # Change button state during calculation
        self.calc_btn.config(state="disabled")
        self.calc_btn.config(text="Calculating...")
        self.update()

        # Get inputs
        rumus = self.rumus_entry.get().strip()
        t_str = self.t_entry.get().strip()
        step_str = self.step_entry.get().strip()

        # Clear log
        self.clear_log()

        # Validate inputs
        if not rumus:
            self.log("Please enter a function", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        if not t_str:
            self.log("Please enter a value for t", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        if not step_str:
            self.log("Please enter a step size", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        try:
            t = float(t_str)
            step = float(step_str)
            if step <= 0:
                raise ValueError("Step must be positive")
        except ValueError as e:
            self.log(f"Invalid number: {str(e)}", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        # Validation checks
        self.log(f"Validating function: {rumus}")

        if not check_allowed_chars(rumus):
            self.log("Error: Function contains illegal characters", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        if not check_parentheses(rumus):
            self.log("Error: Parentheses mismatch", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        if not check_operator(rumus):
            self.log("Error: Operator misuse detected", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        if not check_variable_t(rumus):
            self.log("Error: Variable 't' not found in function", "error")
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")
            return

        # Convert syntax
        original_rumus = rumus
        rumus = rumus.replace("e^", "math.exp")
        rumus = rumus.replace("^", "**")

        self.log(f"Function converted to: {rumus}")
        self.log(f"Calculating derivative at t = {t} with h = {step}")

        try:
            # Perform calculations
            forward_result = foward(rumus, t, step)
            backward_result = backward(rumus, t, step)
            central_result = central(rumus, t, step)

            # Update results with formatting
            self.result_vars[0].set(f"{forward_result:.8f}")
            self.result_vars[1].set(f"{backward_result:.8f}")
            self.result_vars[2].set(f"{central_result:.8f}")

            # Color code based on consistency
            results = [forward_result, backward_result, central_result]
            avg = sum(results) / len(results)

            for i, label in enumerate(self.result_labels):
                diff = abs(results[i] - avg)
                if diff < 1e-6:
                    label.config(fg=self.success_color)
                elif diff < 1e-3:
                    label.config(fg="#ff9800")
                else:
                    label.config(fg=self.error_color)

            self.log(f"Forward difference:  {forward_result:.8f}", "success")
            self.log(f"Backward difference: {backward_result:.8f}", "success")
            self.log(f"Central difference:  {central_result:.8f}", "success")
            self.log("Calculation completed successfully", "success")

        except Exception as e:
            error_msg = str(e)
            self.log(f"Calculation error: {error_msg}", "error")
            self.result_vars[0].set("Error")
            self.result_vars[1].set("Error")
            self.result_vars[2].set("Error")

        finally:
            # Restore button state
            self.calc_btn.config(state="normal")
            self.calc_btn.config(text="Calculate Derivative")


# ===================== MAIN =====================
if __name__ == "__main__":

    # Original UI
    # app = DiffUI()

    # Enhanced UI 
    app = EnhancedDiffUI()

    app.mainloop()