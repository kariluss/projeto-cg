class Matrix:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.data = data or [[0 for _ in range(cols)] for _ in range(rows)]

    def __matmul__(self, other):
        result = Matrix(self.rows, other.cols)

        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result
    
    @property
    def T(self):
        t = [list(t) for t in list(zip(*self.data))]
        return Matrix(len(t), len(t[0]), t)

# escala = Matrix(3, 3, [[2,0,0],[0,2,0],[0,0,1]])
# pontos  = Matrix(3, 6, [[1,2,1],[4,5,1],[7,8,1],[3,3,1],[1,1,1],[2,8,1]])
# escalado = escala @ pontos.T -> precisa transpor para ser posto no modelo colunar onde os vetores estão nas colunas "em pé"
# escalado.T.data

def get_identity_matrix(n=3):
    return Matrix(n, n, [[1 if i == j else 0 for j in range(n)] for i in range(n)])

def get_translation_matrix(tx, ty):
    return Matrix(3, 3, [[1, 0, tx], [0, 1, ty], [0, 0, 1]])

def get_rotation_matrix(angle):
    return Matrix(3, 3, [[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]])

def get_scale_matrix(sx, sy):
    return Matrix(3, 3, [[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

def get_shear_matrix(sx, sy):
    return Matrix(3, 3, [[1, sx, 0], [sy, 1, 0], [0, 0, 1]])

def get_reflection_matrix(axis):
    if axis == 'x':
        return Matrix(3, 3, [[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif axis == 'y':
        return Matrix(3, 3, [[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif axis == 'origin':
        return Matrix(3, 3, [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    else:
        raise ValueError('Invalid axis')