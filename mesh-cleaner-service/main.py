from pipeline.runner import process_mesh

input_file = 'meshes/input/example.obj'
output_file = 'meshes/output/processed_example.obj'

if __name__ == "__main__":
    process_mesh(input_file, output_file)
