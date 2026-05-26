import random
import time

print("===================================")
print("🚚 SYMULATOR KURIERA 2D - CITY RUN")
print("===================================\n")

# -----------------------------
# STARTOWE PARAMETRY
# -----------------------------
name = input("Nazwa kuriera: ")

def get_int(prompt, default):
    try:
        return int(input(prompt))
    except:
        return default

x = get_int("Start X: ", 0)
y = get_int("Start Y: ", 0)
energy = get_int("Początkowa energia: ", 25)
world_size = get_int("Rozmiar miasta (np. 10): ", 10)
difficulty = get_int("Poziom trudności (1-3): ", 1)

max_steps = 20 + difficulty * 5

# cel
target_x = random.randint(-world_size, world_size)
target_y = random.randint(-world_size, world_size)

# historia
history = []
events_log = []

print("\n=== MISJA ROZPOCZĘTA ===")
print(f"Kurier: {name}")
print(f"Start: ({x}, {y})")
print(f"Cel: ({target_x}, {target_y})")
print(f"Granice świata: [-{world_size}, {world_size}]")
print(f"Limit kroków: {max_steps}")
print("===================================\n")

# -----------------------------
# ELEMENTY ŚWIATA
# -----------------------------
def world_event():
    r = random.randint(1, 100)

    if r <= 12:
        return ("🌧 Burza", -4, "energy")
    elif r <= 22:
        return ("🚧 Korek", -3, "energy")
    elif r <= 30:
        return ("⚡ Energia +", +5, "energy")
    elif r <= 35:
        return ("💨 Wiatr (przesunięcie)", 0, "move")
    return None


def world_object():
    r = random.randint(1, 100)

    if r <= 10:
        return "🔋 Stacja ładowania"
    elif r <= 18:
        return "🛑 Blokada drogi"
    elif r <= 25:
        return "⚡ Skrót"
    elif r <= 28:
        return "📦 Znaleziona paczka (+punkty)"
    return None


def clamp(x, y):
    if x > world_size:
        x = world_size
    if x < -world_size:
        x = -world_size
    if y > world_size:
        y = world_size
    if y < -world_size:
        y = -world_size
    return x, y


# -----------------------------
# SYMULACJA
# -----------------------------
for step in range(1, max_steps + 1):

    print("\n-----------------------------------")
    print(f"KROK {step}")
    print("-----------------------------------")
    print(f"Pozycja: ({x}, {y})")
    print(f"Energia: {energy}")

    # warunki końca
    if energy <= 0:
        print("\n❌ KONIEC: brak energii")
        break

    if (x, y) == (target_x, target_y):
        print("\n🎯 SUKCES: paczka dostarczona!")
        break

    move = input("Ruch (W/A/S/D): ").lower()

    x_before, y_before = x, y
    energy_before = energy

    # koszt ruchu zależny od trudności
    energy -= difficulty

    # ruch
    if move == "w":
        y += 1
    elif move == "s":
        y -= 1
    elif move == "a":
        x -= 1
    elif move == "d":
        x += 1
    else:
        print("❗ Brak ruchu (zły input)")

    # granice świata
    x, y = clamp(x, y)

    # obiekt świata
    obj = world_object()
    if obj:
        print(f"📍 Obiekt: {obj}")
        if obj == "🔋 Stacja ładowania":
            energy += 6
        elif obj == "🛑 Blokada drogi":
            energy -= 2
        elif obj == "⚡ Skrót":
            x += random.choice([-2, 2])
            y += random.choice([-2, 2])
        elif obj == "📦 Znaleziona paczka (+punkty)":
            energy += 3

    # zdarzenie losowe
    ev = world_event()
    if ev:
        print(f"⚠ ZDARZENIE: {ev[0]}")
        if ev[2] == "energy":
            energy += ev[1]
        elif ev[2] == "move":
            x += random.choice([-1, 1])
            y += random.choice([-1, 1])

        events_log.append(ev[0])

    # zapis historii
    history.append((step, (x_before, y_before), (x, y), energy_before, energy))

    x, y = clamp(x, y)

    print(f"Zmiana: ({x_before}, {y_before}) -> ({x}, {y})")
    print(f"Energia po kroku: {energy}")

# -----------------------------
# RAPORT KOŃCOWY
# -----------------------------
print("\n===================================")
print("📊 RAPORT KOŃCOWY")
print("===================================")

print(f"Kurier: {name}")
print(f"Start: (0,0) approx / {x, y}")
print(f"Cel: ({target_x}, {target_y})")
print(f"Pozycja końcowa: ({x}, {y})")
print(f"Kroki wykonane: {step}")
print(f"Energia końcowa: {energy}")

print("\n📜 Historia ruchów:")
for h in history[-5:]:
    print(h)

print("\n⚠ Zdarzenia:")
print(events_log if events_log else "Brak")

# wynik
if (x, y) == (target_x, target_y):
    print("\n🏆 WYNIK: SUKCES")
elif energy <= 0:
    print("\n💀 WYNIK: PORAŻKA")
else:
    print("\n📦 WYNIK: CZĘŚCIOWY SUKCES (limit kroków)")

print("\n=== KONIEC MISJI ===")