class OBJ:
    def __init__(self, file_path):
        self.vertices = []
        self.faces = []
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    # Procesa vértices
                    vertex = list(map(float, line[2:].strip().split()))
                    self.vertices.append(vertex)
                elif line.startswith('f '):
                    # Procesa caras
                    face = [int(vertex.split('/')[0]) - 1 for vertex in line[2:].strip().split()]
                    self.faces.append(face)
