# Módulo destinado a escribir las estructuras de datos que serán ser utilizadas


class Node:

    def __init__(self, value=None):
        self.value = value
        self.next = None

    def __lt__(self, other):
        if self.value < other.value:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False


class Iterator:
    """As seen at https://stackoverflow.com/questions/19721334/
    python-iterators-on-linked-list-elements"""
    def __init__(self, head):
        self.current = head

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        else:
            current = self.current
            self.current = self.current.next
            return current.value


class Listirijilla:

    def __init__(self, arg=None):
        self.head = None
        self.tail = None
        if arg:
            self.append(arg)

    def append(self, value):
        new = Node(value)
        if not self.head:
            self.head = new
            self.tail = self.head
        else:
            self.tail.next = new
            self.tail = self.tail.next

    def __getitem__(self, position):
        current_node = self.head
        for node in range(position):
            if current_node:
                current_node = current_node.next
        if not current_node:
            raise IndexError("Posición fuera de rango")
        return current_node.value

    def __setitem__(self, position, value):
        """As seen at: https://github.com/IIC2233/contenidos/blob/master/
        semana-03/01-arboles%20y%20listas%20ligadas.ipynb"""
        if position > len(self):
            raise IndexError("Posición fuera de rango")
        current_node = self.head
        if position == 0:
            self.head.value = value
        else:
            for node in range(position):
                if current_node:
                    current_node = current_node.next
            if current_node is not None:
                current_node.value = value

    def __len__(self):
        total = 0
        current = self.head
        if current is None:
            return total
        while current:
            current = current.next
            total += 1
        return total

    def __repr__(self):
        if not len(self):
            return "[]"
        rep = '['
        current = self.head

        while current:
            rep += '{} , '.format(current.value)
            current = current.next
        rep = rep[:-3]
        rep += "]"
        return rep

    def __iter__(self):
        return Iterator(self.head)

    def __add__(self, other):
        if not isinstance(other, Listirijilla):
            raise TypeError("Sólo puedes sumar una lista con otra")
        new = Listirijilla()
        for value in self:
            new.append(value)
        for value in other:
            new.append(value)
        return new

    def sort(self):
        """As seen at https://stackoverflow.com/questions/18262306/
        quicksort-with-python"""
        def quick(sub_lista):
            if len(sub_lista) > 1:
                less = Listirijilla()
                equal = Listirijilla()
                greater = Listirijilla()
                pivot = sub_lista.head
                current = sub_lista.head
                while current:
                    if current < pivot:
                        less.append(current.value)
                    if current == pivot:
                        equal.append(current.value)
                    if current > pivot:
                        greater.append(current.value)
                    current = current.next
                return quick(less) + equal + quick(greater)
            else:
                return sub_lista
        aux = quick(self)
        self.head = aux.head
        self.tail = aux.tail

    def popleft(self):
        if len(self):
            aux = self.head
            self.head = self.head.next
            return aux.value
        else:
            raise IndexError

    def remove(self, value):
        anterior = self.head
        if self.head is None:
            return
        if self.head.value == value:
            self.head = self.head.next
            return
        current = self.head.next
        while current.value is not None:
            if current.value == value:
                anterior.next = current.next
                return
            anterior = current
            current = current.next


class SamePlayerError(Exception):

    def __init__(self):
        super().__init__("No existe la afinidad de un jugador consigo mismo")


class NotConectedError(Exception):

    def __init__(self):
        super().__init__("Los jugadores no tienen grado uno de relación")


"""As seen at:
-https://stackoverflow.com/questions/39286116/
python-class-behaves-like-dictionary-or-list-data-like
-https://intelligentjava.wordpress.com/2016/10/19/
introduction-to-hash-tables/"""


# Esta tabla de hash asume hash perfecto.
class HashTable(object):

    def __init__(self):
        self._hashes = Listirijilla()
        self._values = Listirijilla()

    def __getitem__(self, key):
        h = hash(key)
        position = 0
        for hsh in self._hashes:
            if hsh == h:
                return self._values[position]
            position += 1
        raise KeyError

    # este set sirve para añadir rápido si sabemos que no existe la llave
    def fast_set(self, key, value):
        h = hash(key)
        self._hashes.append(h)
        self._values.append(value)

    def __setitem__(self, key, value):
        h = hash(key)
        position = 0
        for hsh in self._hashes:
            if hsh == h:
                self._values[position] = value
                break
            position += 1
        else:
            self._hashes.append(h)
            self._values.append(value)

    def __len__(self):
        return len(self._hashes)