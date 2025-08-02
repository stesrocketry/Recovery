import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import trimesh

# -----------------------------
# GORE PATTERN (PDF)
# -----------------------------
def calculate_hemispherical_gore_coordinates(radius, num_gores, num_points=100):
    gore_height = (math.pi * radius) / 2.0
    coordinates = []
    for i in range(num_points + 1):
        y = (i / num_points) * gore_height
        phi = (i / num_points) * (math.pi / 2)
        r_slice = radius * math.sin(phi)
        x = (math.pi * r_slice) / num_gores
        coordinates.append((x, y))
    return coordinates

def plot_and_save_gore(parachute_diameter, radius, num_gores, seam_cm, seam_m, spill_cm, spill_m):
    gore_points = calculate_hemispherical_gore_coordinates(radius, num_gores)
    x_right = [p[0] for p in gore_points]
    y_coords = [p[1] for p in gore_points]
    x_left = [-x for x in x_right]

    x_full = x_left[::-1] + [x_right[0]] + x_right
    y_full = y_coords[::-1] + [y_coords[0]] + y_coords

    x_right_seam = [x + seam_m for x in x_right]
    x_left_seam = [-x - seam_m for x in x_right]
    x_full_seam = x_left_seam[::-1] + [x_right_seam[0]] + x_right_seam

    plt.figure(figsize=(8, 12))
    plt.plot(x_full, y_full, color='red', linewidth=1.5, label='Gore Pattern (No Seam)')
    plt.fill(x_full, y_full, color='red', alpha=0.1)
    plt.plot(x_full_seam, y_full, color='black', linewidth=1.5, label=f'Seam Allowance: {seam_cm:.1f} cm')
    plt.axvline(0, color='gray', linestyle=':', linewidth=0.8, label='Centerline')

    if spill_m > 0:
        spill_radius = (math.pi * (spill_m / 2)) / num_gores
        circle = Circle((0, 0), radius=spill_radius, fill=False, color='blue', linestyle='--', linewidth=1.0, label='Spill Hole')
        plt.gca().add_patch(circle)

    plt.title(f'Hemispherical Gore\nDiameter={parachute_diameter:.2f}m, Gores={num_gores}, Spill={spill_cm:.1f}cm')
    plt.xlabel("Width (m)")
    plt.ylabel("Height (m)")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    pdf_name = f"gore_D{parachute_diameter:.2f}m_G{num_gores}_SA{seam_cm:.1f}cm.pdf"
    plt.savefig(pdf_name)
    plt.close()
    print(f"✅ Gore pattern saved as: {pdf_name}")

# -----------------------------
# PARAMETRIC 3D PARACHUTE (STL)
# -----------------------------
def generate_gore_mesh(radius, phi_steps, theta_steps, num_gores, inflation_factor):
    phi = np.linspace(0, np.pi / 2, phi_steps)
    theta = np.linspace(-np.pi / num_gores, np.pi / num_gores, theta_steps)
    phi, theta = np.meshgrid(phi, theta)
    x = radius * np.sin(phi) * np.sin(theta)
    y = radius * np.sin(phi) * np.cos(theta)
    z = radius * inflation_factor * np.cos(phi)
    return x, y, z

def assemble_full_parachute(radius, num_gores, phi_steps, theta_steps, inflation_factor):
    all_vertices = []
    all_faces = []
    vertex_offset = 0

    for g in range(num_gores):
        angle = g * 2 * np.pi / num_gores
        x, y, z = generate_gore_mesh(radius, phi_steps, theta_steps, num_gores, inflation_factor)
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)
        vertices = np.stack((x_rot, y_rot, z), axis=-1).reshape(-1, 3)
        all_vertices.append(vertices)

        rows, cols = x.shape
        for i in range(rows - 1):
            for j in range(cols - 1):
                a = vertex_offset + i * cols + j
                b = a + 1
                c = a + cols
                d = c + 1
                all_faces.append([a, b, c])
                all_faces.append([b, d, c])
        vertex_offset += vertices.shape[0]

    all_vertices = np.vstack(all_vertices)
    all_faces = np.array(all_faces)
    return all_vertices, all_faces

def export_parachute_3d_mesh(radius, num_gores, spill_m, filename='parachute.stl', inflation_factor=1.1):
    phi_steps = 100
    theta_steps = 50

    vertices, faces = assemble_full_parachute(radius, num_gores, phi_steps, theta_steps, inflation_factor)

    if spill_m > 0:
        radial_distance = np.linalg.norm(vertices[:, :2], axis=1)
        keep_mask = radial_distance > (spill_m / 2)

        old_to_new = -np.ones(len(keep_mask), dtype=int)
        new_indices = np.where(keep_mask)[0]
        old_to_new[new_indices] = np.arange(len(new_indices))

        vertices = vertices[keep_mask]
        filtered_faces = []
        for face in faces:
            if all(keep_mask[face]):
                new_face = [old_to_new[idx] for idx in face]
                filtered_faces.append(new_face)
        faces = np.array(filtered_faces)

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.export(filename)
    print(f"✅ 3D parachute mesh saved as: {filename}")

# -----------------------------
# MAIN USER INTERFACE
# -----------------------------
try:
    diameter = float(input("Enter parachute diameter in meters (e.g., 2.0): "))
    if diameter <= 0:
        raise ValueError("Diameter must be positive.")
    radius = diameter / 2.0

    num_gores = int(input("Enter number of gores (e.g., 12): "))
    if num_gores < 1:
        raise ValueError("Gores must be at least 1.")

    seam_cm = float(input("Enter seam allowance in cm (e.g., 1.5): "))
    seam_m = seam_cm / 100.0
    if seam_m < 0:
        raise ValueError("Seam allowance cannot be negative.")

    spill_cm = float(input("Enter spill hole diameter in cm (0 for none): "))
    spill_m = spill_cm / 100.0
    if spill_m < 0:
        raise ValueError("Spill hole cannot be negative.")

except ValueError as e:
    print(f"❌ Input error: {e}")
    exit()

# Run generator
plot_and_save_gore(diameter, radius, num_gores, seam_cm, seam_m, spill_cm, spill_m)
export_parachute_3d_mesh(radius, num_gores, spill_m, filename=f"parachute_D{diameter:.2f}m_G{num_gores}.stl")
