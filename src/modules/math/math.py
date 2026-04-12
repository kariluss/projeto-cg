from math import cos, sin

class Matrix:
    """Matrix class
    
    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        data (list): matrix data

    Methods:
        __matmul__(self, other): matrix multiplication
        T: transpose matrix
    """
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.data = data or [[0 for _ in range(cols)] for _ in range(rows)]

    def __matmul__(self, other):
        """matrix multiplication. About this overload, see: https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
        Args:
            other (Matrix): other matrix, must have the same number of rows as the number of columns of self
        Returns:
            Matrix: result matrix
        """
        if self.cols != other.rows:
            raise ValueError(f'Number of columns of self ({self.cols}) must be equal to the number of rows of other ({other.rows})')
        ,
        result = Matrix(self.rows, other.cols)

        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result
    
    @property
    def T(self):
        """transpose matrix
        Returns:
            Matrix: transpose matrix
        """
        t = [list(t) for t in list(zip(*self.data))]
        return Matrix(len(t), len(t[0]), t)

# escala = Matrix(3, 3, [[2,0,0],[0,2,0],[0,0,1]])
# pontos  = Matrix(3, 6, [[1,2,1],[4,5,1],[7,8,1],[3,3,1],[1,1,1],[2,8,1]])
# escalado = escala @ pontos.T -> precisa transpor para ser posto no modelo colunar onde os vetores estão nas colunas "em pé"
# escalado.T.data

def get_identity_matrix(n=3):
    """identity matrix
    Args:
        n (int): size of the matrix
    Returns:
        Matrix: identity matrix
    """
    return Matrix(n, n, [[1 if i == j else 0 for j in range(n)] for i in range(n)])

def get_translation_matrix(tx, ty):
    """translation matrix
    Args:
        tx (float): translation in x
        ty (float): translation in y
    Returns:
        Matrix: translation matrix
    """
    return Matrix(3, 3, [[1, 0, tx], [0, 1, ty], [0, 0, 1]])

def get_rotation_matrix(angle):
    """rotation matrix

    Args:
        angle (float): angle in radians

    Returns:
        Matrix: rotation matrix
    """
    return Matrix(3, 3, [[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]])

def get_scale_matrix(sx, sy):
    """scale matrix

    Args:
        sx (float): scale factor in x
        sy (float): scale factor in y

    Returns:
        Matrix: scale matrix
    """
    return Matrix(3, 3, [[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

def get_shear_matrix(sx, sy):
    """shear matrix

    Args:
        sx (float): shear factor in x
        sy (float): shear factor in y

    Returns:
        Matrix: shear matrix
    """
    return Matrix(3, 3, [[1, sx, 0], [sy, 1, 0], [0, 0, 1]])

def get_reflection_matrix(axis):
    """reflection matrix
    Args:
        axis (str): axis of reflection

    Returns:
        Matrix: reflection matrix
    """
    if axis == 'x':
        return Matrix(3, 3, [[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif axis == 'y':
        return Matrix(3, 3, [[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif axis == 'origin':
        return Matrix(3, 3, [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    else:
        raise ValueError('Invalid axis')