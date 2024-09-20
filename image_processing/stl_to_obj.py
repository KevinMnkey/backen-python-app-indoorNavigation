from stl import mesh

def convert_stl_to_obj(stl_file_path, obj_file_path):
   
    your_mesh = mesh.Mesh.from_file(stl_file_path)

   
    with open(obj_file_path, 'w') as obj_file:
      
        for vertex in your_mesh.vectors.reshape(-1, 3):
            obj_file.write(f'v {vertex[0]} {vertex[1]} {vertex[2]}\n')
        

        num_faces = len(your_mesh.vectors)
        for i in range(num_faces):
            
            base_index = i * 3 + 1
            obj_file.write(f'f {base_index} {base_index + 1} {base_index + 2}\n')

    print(f"Archivo OBJ guardado en: {obj_file_path}")

