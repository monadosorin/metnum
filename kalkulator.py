import math

def foward(rumus, t, step):
    print("\n\nFoward : ")
    # Hitung f(t) dan f(t+h)
    f1 = eval(rumus, {"math": math}, {"t": t})
    f2 = eval(rumus, {"math": math}, {"t": t + step})

    print(f"f({t})     = {f1}")
    print(f"f({t}+{step}) = {f2}")

    # a(x) 
    hasil = (f2 - f1)/step
    return hasil

def backward(rumus, t, step):
    print("\n\nBackward : ")
    # Hitung f(t) dan f(t-h)
    f1 = eval(rumus, {"math": math}, {"t": t})
    f2 = eval(rumus, {"math": math}, {"t": t - step})

    print(f"f({t})     = {f1}")
    print(f"f({t}-{step}) = {f2}")

    # a(x) 
    hasil = (f1 - f2)/step
    return hasil

def central(rumus, t, step):
    print("\n\nCentral : ")
    # Hitung f(t+h) dan f(t-h)
    f1 = eval(rumus, {"math": math}, {"t": t + step})
    f2 = eval(rumus, {"math": math}, {"t": t - step})

    print(f"f({t}+{step}) = {f1}")
    print(f"f({t}-{step}) = {f2}")

    # a(x) 
    hasil = (f1 - f2)/(2*step)
    return hasil

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

def check_parentheses(rumus):
    stack = 0
    for char in rumus:
        if char == "(":
            stack += 1
        elif char == ")":
            stack -= 1
            if stack < 0:
                return False
    return stack == 0

def check_empty_parentheses(rumus):
    rumus = rumus.replace(" ", "")
    return "()" not in rumus

def check_operator(rumus):
    operators = "+-*/^"
    
    # hapus spasi
    rumus = rumus.replace(" ", "")
    
    # awal / akhir
    if rumus[0] in operators or rumus[-1] in operators:
        return False
    
    # cek berurutan
    for i in range(len(rumus) - 1):
        if rumus[i] in operators and rumus[i+1] in operators:
            # izinkan operator +-
            if not (rumus[i] in "*/^" and rumus[i+1] == "-"):
                return False
    return True

def check_allowed_chars(rumus):
    allowed = "0123456789+-*/^.()t e"
    
    for char in rumus:
        if char not in allowed:
            return False
    return True

def check_variable_t(rumus):
    return "t" in rumus

def check_sebelah_t(rumus):
    rumus = rumus.replace(" ", "")
    operators = "+-*/^"
    n = len(rumus)

    for i in range(n):
        if rumus[i] == "t":

            # cek kiri
            if i > 0:
                kiri = rumus[i - 1]
                if kiri not in operators + "(":
                    return False

            # cek kanan
            if i < n - 1:
                kanan = rumus[i + 1]
                if kanan not in operators + ")":
                    return False

    return True

# --------------------------------------------------------------------------------------
while(True):
    # Input rumus custom
    rumus = input("Rumus : V(t) = ")
    # rumus = "((9.81*70)/12)*(1-e^(-(12/70)*t))"       # rumus dummy
    print("V(t) = " + rumus)

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

    break


# Input posisi + step
t = input_t("t : ")
step = input_step("Step : ")


# Special variable checker
if "e^" in rumus:
    rumus = rumus.replace("e^", "math.exp")


# debug Rumus
print(rumus)

# Output
print("a(t) = " + str(foward(rumus, t, step)))
print("a(t) = " + str(backward(rumus, t, step)))
print("a(t) = " + str(central(rumus, t, step)))

