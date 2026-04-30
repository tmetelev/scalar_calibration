import math

# золотое сечение
phi = (1 + math.sqrt(5)) / 2
a = 1 / phi

vertices = []

# (±1, ±1, ±1)
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            vertices.append((x, y, z))

# (0, ±1/φ, ±φ)
for y in [-a, a]:
    for z in [-phi, phi]:
        vertices.append((0, y, z))

# (±1/φ, ±φ, 0)
for x in [-a, a]:
    for y in [-phi, phi]:
        vertices.append((x, y, 0))

# (±φ, 0, ±1/φ)
for x in [-phi, phi]:
    for z in [-a, a]:
        vertices.append((x, 0, z))


# --- 1. ФИЗИЧЕСКАЯ СИСТЕМА ---
def to_physical(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    theta = math.acos(z / r)        # от оси Z
    phi_angle = math.atan2(y, x)    # азимут
    return theta, phi_angle


# --- 2. МАТЕМАТИЧЕСКАЯ СИСТЕМА ---
def to_mathematical(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    theta = math.atan2(y, x)        # азимут
    phi_angle = math.asin(z / r)    # от плоскости XY
    return theta, phi_angle


print("Физическая система:")
for i, (x, y, z) in enumerate(vertices):
    theta, phi_angle = to_physical(x, y, z)
    print(f"{i+1}: θ={theta:.5f}, φ={phi_angle:.5f}")

print("\nМатематическая система:")
for i, (x, y, z) in enumerate(vertices):
    theta, phi_angle = to_mathematical(x, y, z)
    print(f"{i+1}: θ={theta:.5f}, φ={phi_angle:.5f}")