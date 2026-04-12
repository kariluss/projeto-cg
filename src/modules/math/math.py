class Matrix:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.data = data or [[0 for _ in range(cols)] for _ in range(rows)]

    def __matmul__(self, other):
        # Esta única função resolve:
        # 1. Matriz 3x3 @ Matriz 3x3
        # 2. Matriz 3x3 @ Matriz 3xN (Batch de pontos)
        # 3. Matriz 3x3 @ Matriz 3x1 (único ponto)
        
        result = Matrix(self.rows, other.cols)
        
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result