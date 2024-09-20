import svgpathtools
import numpy as np
from stl import mesh

def svg_to_paths(svg_file):
    paths, _ = svgpathtools.svg2paths(svg_file)
    return paths

def extrude_path_to_3d(path, height):
    vertices = []
    faces = []

    base_vertices = []
    top_vertices = []

    scale_factor = 0.01  # Ajustar la escala según sea necesario

    for segment in path:
        for point in segment:
            x, y = point.real * scale_factor, point.imag * scale_factor
            base_vertices.append([x, y, 0])  # Base (Z = 0)
            top_vertices.append([x, y, height * scale_factor])  # Altura (Z = height)

    num_base_vertices = len(base_vertices)
    vertices.extend(base_vertices)
    vertices.extend(top_vertices)

    # Crear las caras del modelo 3D
    for i in range(num_base_vertices):
        next_i = (i + 1) % num_base_vertices  # Para cerrar el borde
        # Añadir las caras laterales (asegúrate de que el orden sea correcto para las normales)
        faces.append([i, next_i, num_base_vertices + next_i])  # Cara lateral
        faces.append([i, num_base_vertices + next_i, num_base_vertices + i])  # Otra cara lateral

    faces = np.array(faces)

    # Crear la malla con las caras
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = vertices[face[j]]

    return mesh_data

def convert_svg_to_stl(svg_file, stl_file):
    paths = svg_to_paths(svg_file)

    all_faces = []
    for path in paths:
        mesh_data = extrude_path_to_3d(path, height=30)  # Ajustar la altura según sea necesario
        all_faces.extend(mesh_data.vectors)

    all_faces = np.array(all_faces)
    mesh_data = mesh.Mesh(np.zeros(all_faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(all_faces):
        for j in range(3):
            mesh_data.vectors[i][j] = face[j]

    # Guardar el archivo STL
    mesh_data.save(stl_file)

    print(f"Archivo STL guardado como '{stl_file}'.")

# Uso del script
if __name__ == "__main__":
    svg_file = 'input.svg'  # Reemplaza con la ruta a tu archivo SVG
    stl_file = 'output.stl'  # Reemplaza con la ruta para guardar el archivo STL
    convert_svg_to_stl(svg_file, stl_file)
