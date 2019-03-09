import funciones


class MetaAuto(type):

    _instances = []
    def __new__(meta, nombre, bases, clsdic):
        clsdic["piezas"] = funciones.crear_piezas()
        clsdic["definir_estado_piezas"] = funciones.definir_estado_piezas
        return super().__new__(meta, nombre, bases, clsdic)

    def __init__(cls, name, bases, clsdic):
        super().__init__(name, bases, clsdic)

    def __call__(cls, *args, **kwargs):
        ret = None
        if len(cls._instances) < 3:
            ret = super().__call__(*args, **kwargs)
            cls._instances.append(ret)
        return ret


class MetaTrabajador(type):

    def __new__(meta, nombre, bases, clsdic):
        del clsdic["revizar_ztado"]
        clsdic["revisar_estado"] = funciones.revisar_estado
        clsdic["reparar"] = funciones.reparar
        return super().__new__(meta, nombre, bases, clsdic)

    def __init__(cls, name, bases, clsdic):
        super().__init__(name, bases, clsdic)

    def __call__(cls, *args, **kwargs):
        """As seen at: https://github.com/IIC2233/contenidos/blob/
        master/semana-07/01-metaclases.ipynb"""
        if not hasattr(cls, "instance"):
            cls.instance = super().__call__(*args, *kwargs)
        return cls.instance
