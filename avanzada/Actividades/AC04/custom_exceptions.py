class ExcesoDeLikes(Exception):

    def __init__(self):
        super().__init__("El video tiene más likes que views")

class TagNulo(Exception):

    def __init__(self):
        super().__init__("El tag del video es de largo 0 o es None")