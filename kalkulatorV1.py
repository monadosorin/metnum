import math

# METODE DIFERENSIAL NUMERIK LOGIC
def foward(rumus, t, step):
    print("\n\nFoward : ")
    # Hitung f(t) dan f(t+h)
    f1 = safe_eval(rumus, t)
    f2 = safe_eval(rumus, t + step)

    if f1 is None or f2 is None:
        return None

    print(f"f({t}) = {f1}")
    print(f"f({t}+{step}) = {f2}")

    return (f2 - f1) / step

def backward(rumus, t, step):
    print("\n\nBackward : ")
    # Hitung f(t) dan f(t-h)
    f1 = safe_eval(rumus, t)
    f2 = safe_eval(rumus, t - step)

    if f1 is None or f2 is None:
        return None

    print(f"f({t})     = {f1}")
    print(f"f({t}-{step}) = {f2}")

    # a(x)
    return (f1 - f2)/step

def central(rumus, t, step):
    print("\n\nCentral : ")
    # Hitung f(t+h) dan f(t-h)
    f1 = safe_eval(rumus, t + step)
    f2 = safe_eval(rumus, t - step)

    if f1 is None or f2 is None:
        return None
    
    print(f"f({t}+{step}) = {f1}")
    print(f"f({t}-{step}) = {f2}")

    # a(x) 
    return (f1 - f2)/(2*step)

def safe_eval(rumus, t):
    try:
        return eval(rumus, {"math": math, "e": math.e}, {"t": t})
    except ZeroDivisionError:
        print("Error: pembagian dengan nol")
        return None
    except Exception:
        print("Error: rumus tidak bisa dihitung")
        return None

# CUSTOM RULE INPUT
def input_t(isi):
    while True:
        try:
            return float(input(isi))
        except ValueError:
            print("Error: input harus berupa angka")

def input_step(isi):
    while True:
        try:
            value = float(input(isi))
            if value <= 0:
                print("Error: step harus lebih besar dari 0")
                continue
            return value
        except ValueError:
            print("Error: input harus berupa angka")


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

            # kiri t
            if i > 0:
                kiri = r[i - 1]
                if kiri.isdigit() or kiri == ")" or kiri == "e":
                    return False

            # kanan t
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

            # kiri e
            if i > 0:
                kiri = r[i - 1]
                if kiri.isdigit() or kiri == ")" or kiri == "t" or kiri == "e":
                    return False

            # kanan e
            if i < n - 1:
                kanan = r[i + 1]

                # e^ boleh
                if kanan == "^":
                    continue

                # e sebagai konstanta
                if kanan.isdigit() or kanan == "t" or kanan == "e":
                    return False

    return True

def tabel_perhitungan(rumus, t, step):
    f_t = safe_eval(rumus, t)
    f_th = safe_eval(rumus, t + step)
    f_tmh = safe_eval(rumus, t - step)

    if None in (f_t, f_th, f_tmh):
        print("Tabel tidak bisa ditampilkan karena error evaluasi.")
        return

    forward = (f_th - f_t) / step
    backward = (f_t - f_tmh) / step
    central = (f_th - f_tmh) / (2 * step)

    print("\nTABEL PERHITUNGAN")
    print("=" * 70)
    print(f"V(t) = {rumus}")
    print(f"t = {t}, h = {step}\n")
    print(f"{'Metode':<10} | {'f(t-h)':<12} | {'f(t)':<12} | {'f(t+h)':<12} | {'Hasil':<12}")
    print("-" * 70)
    print(f"{'Forward':<10} | {'-':<12} | {f_t:<12.6f} | {f_th:<12.6f} | {forward:<12.6f}")
    print(f"{'Backward':<10} | {f_tmh:<12.6f} | {f_t:<12.6f} | {'-':<12} | {backward:<12.6f}")
    print(f"{'Central':<10} | {f_tmh:<12.6f} | {'-':<12} | {f_th:<12.6f} | {central:<12.6f}")
    print("=" * 70)

    return forward, backward, central

# --------------------------------------------------------------------------------------
while(True):
    # Input rumus custom
    rumus = input("Rumus : V(t) = ")
    # rumus = "((9.81*70)/12)*(1-e^(-(12/70)*t))"       # rumus dummy
    # print("V(t) = " + rumus)

    # validator rumus
    if not check_allowed_chars(rumus):
        print("Error: karakter ilegal terdeteksi")
        continue

    if not check_parentheses(rumus):
        print("Error: tanda kurung tidak seimbang")
        continue

    if not check_empty_parentheses(rumus):
        print("Error: tanda kurung kosong () tidak diperbolehkan")
        continue

    if not check_operator(rumus):
        print("Error: operator tidak valid")
        continue

    if not check_variable_t(rumus):
        print("Error: variabel t tidak ditemukan")
        continue

    if not check_sebelah_t(rumus):
        print("Error: gunakan operator di sekitar t")
        continue

    if not check_e_usage(rumus):
        print("Error: penggunaan e tidak valid")
        continue
    
    break


# Input posisi + step
t = input_t("t : ")
step = input_step("Step : ")


# Special variable checker
if "e^" in rumus:
    rumus = rumus.replace("e^", "math.exp")

if "^" in rumus:
    rumus = rumus.replace("^", "**")


# debug Rumus
# print("\n\n"+rumus)

# Output
print("a(t) = " + str(foward(rumus, t, step)))
print("a(t) = " + str(backward(rumus, t, step)))
print("a(t) = " + str(central(rumus, t, step)))

# Tabel perhitungan
fwd, bwd, ctr = tabel_perhitungan(rumus, t, step)