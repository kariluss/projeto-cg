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