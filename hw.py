from abc import ABC, abstractmethod
from typing import List, Optional
import copy
class Printable(ABC):
    """Base abstract class for printable objects."""
    def print_me(self, prefix="", is_last=False, no_slash=False, is_root=False):
        # add = "| " if no_slash else "  "
        add = "+-" if not is_last else "\-"
       
        return prefix + add + str(self) + "\n"
        """Base printing method for the tree structure display.
        Implement properly to display hierarchical structure."""
        result = prefix
        has_prefix = len(prefix) > 0

        if has_prefix:
            result += " " if no_slash else "|"

        if not is_root:
            result += "\\-" if is_last else "+-"

        result += str(self)
        result += "\n"
        return result

#    @abstractmethod
    def clone(self):
        """Create a deep copy of this object."""
        return copy.deepcopy(self)
        
class BasicCollection(Printable):
    """Base class for collections of items."""
    def __init__(self):
        self._items = []
    def add(self, elem):
        self._items.append(elem)
        pass
    def find(self, elem):
        for i, el in enumerate(self._items):
            if el == elem:
                return el#.clone()
        assert False, f'Item {elem} not found'
        
    def clone(self):
        return copy.deepcopy(self)
    def print_me(self, prefix, is_last, no_slash=True):
        add = "+-" if not is_last else "\-"
        res = prefix + add + str(self) + "\n"
#        if not is_last:
#            prefix += padd
        for idx, ch in enumerate(self._items):
            last =  idx == len(self._items) -1
            padd = "| " if not is_last else "  "
            res += ch.print_me(prefix + padd, last)
        return res
        
        

class Component(Printable):
    """Base class for computer components."""
    def __init__(self, numeric_val=0):
        self.numeric_val = numeric_val
    # To be implemented
class Address(Printable):
    """Class representing a network address."""
    def __init__(self, addr):
        self.address = addr

    def validate(self, addr):
        try:
            assert all(map(lambda o: 0 <= o and o < 256, map(int, addr.split('.'))))
        except:
            raise ValueError("Invalid network address")
    def __str__(self):
        return self.address

    

   
class Computer(BasicCollection, Component):
    """Class representing a computer with addresses and components."""
    def __init__(self, name):
        super().__init__()
        self.name = name
    def add_address(self, addr):
        self.add(Address(addr))
        return self
    def add_component(self, comp):
        self.add(comp)
        return self
       
    @property
    def components(self):
        return self._items[1:] # кропнули ip
    def __str__(self):
        return f"Host: {self.name}"

    
    def __eq__(self, other):
        return self.name == other.name
        
        
class Network(BasicCollection):
    """Class representing a network of computers."""
    def __init__(self, name):
        super().__init__()
        self.name = name
    def add_computer(self, comp):
        self.add(comp)
        return self
    def find_computer(self, name):
        # To be implemented
        return self.find(Computer(name))
    # Другие методы...
    def __str__(self):
        result = f"Network: {self.name}\n"
        
        
        cc = len(self._items)
        for idx in range(cc):
            result += self._items[idx].print_me("", idx == cc - 1)

        
        return result.rstrip()

class Partition(Component):
    def __init__(self, size, name, idx):
        super().__init__(idx)
        self.size = size
        self.name = name
    def __str__(self):
        return f"[{self.numeric_val}]: {self.size} GiB, {self.name}"
    
class Disk(BasicCollection, Component):
    """Disk component class with partitions."""
    # Определение типов дисков
    SSD = 0
    MAGNETIC = 1
    def __init__(self, storage_type: int, size: int):
        # Initialize properly
        super().__init__()
        if (storage_type not in [self.SSD, self.MAGNETIC]):
            raise ValueError("Invalid storage type")

        self._storage_type = storage_type
        self._size = size

    def __str__(self):
        return ("HDD" if self._storage_type == 1 else "SSD") + f", {self._size} GiB"

    def add_partition(self, size: int, name: str):
        remain = self._size - sum(t.size for t in self._items)

        if size > remain:
            raise ValueError("Failed to add partition")
        self.add(Partition(size, name, len(self._items)))
        return self
        
class CPU(Component):
    """CPU component class."""
    def __init__(self, cores, mhz):
        self._cores = cores
        self._mhz = mhz
        
    def __str__(self):
        return f"CPU, {self._cores} cores @ {self._mhz}MHz"

class Memory(Component):
    """Memory component class."""
    def __init__(self, size: int):
        self._size = size
        
    def __str__(self):
        return f"Memory, {self._size} MiB"

# Пример использования (может быть неполным или содержать ошибки)
def main():
    # Создание тестовой сети
    n = Network("MISIS network")
    # Добавляем первый сервер с одним CPU и памятью
    n.add_computer(
        Computer("server1.misis.ru")
        .add_address("192.168.1.1")
        .add_component(CPU(4, 2500))
        .add_component(Memory(16000))
    )
    # Добавляем второй сервер с CPU и HDD с разделами
    n.add_computer(
        Computer("server2.misis.ru")
        .add_address("10.0.0.1")
        .add_component(CPU(8, 3200))
        .add_component(
            Disk(Disk.MAGNETIC, 2000)
            .add_partition(500, "system")
            .add_partition(1500, "data")
        )
    )
    # Выводим сеть для проверки форматирования
    print("=== Созданная сеть ===")
    print(n)
    # Тест ожидаемого вывода
    expected_output = """Network: MISIS network
+-Host: server1.misis.ru
| +-192.168.1.1
| +-CPU, 4 cores @ 2500MHz
| \-Memory, 16000 MiB
\-Host: server2.misis.ru
  +-10.0.0.1
  +-CPU, 8 cores @ 3200MHz
  \-HDD, 2000 GiB
    +-[0]: 500 GiB, system
    \-[1]: 1500 GiB, data"""
    assert str(n) == expected_output, "Формат вывода не соответствует ожидаемому"
    print("✓ Тест формата вывода пройден")
    # Тестируем глубокое копирование
    print("\n=== Тестирование глубокого копирования ===")
    x = n.clone()
    # Тестируем поиск компьютера
    print("Поиск компьютера server2.misis.ru:")
    c = x.find_computer("server2.misis.ru")
    print(c)
    # Модифицируем найденный компьютер в копии
    print("\nДобавляем SSD к найденному компьютеру в копии:")
    c.add_component(
        Disk(Disk.SSD, 500)
        .add_partition(500, "fast_storage")
    )
    # Проверяем, что оригинал не изменился
    print("\n=== Модифицированная копия ===")
    print(x)
    print("\n=== Исходная сеть (должна остаться неизменной) ===")
    print(n)
    # Проверяем ассерты для тестирования системы
    print("\n=== Выполнение тестов ===")
    # Тест поиска
    assert x.find_computer("server1.misis.ru") is not None, "Компьютер не найден"
    print("✓ Тест поиска пройден")
    # Тест независимости копий
    original_server2 = n.find_computer("server2.misis.ru")
    modified_server2 = x.find_computer("server2.misis.ru")
    original_components = sum(1 for _ in original_server2.components)
    modified_components = sum(1 for _ in modified_server2.components)
    assert original_components == 2, f"Неверное количество компонентов в оригинале: {original_components}"
    assert modified_components == 3, f"Неверное количество компонентов в копии: {modified_components}"
    print("✓ Тест независимости копий пройден")
    # Проверка типов дисков
    disk_tests = [
        (Disk(Disk.SSD, 256), "SSD"),
        (Disk(Disk.MAGNETIC, 1000), "HDD")
    ]
    for disk, expected_type in disk_tests:
        assert expected_type in str(disk), f"Неверный тип диска в выводе: {str(disk)}"
    print("✓ Тест типов дисков пройден")
    print("\nВсе тесты пройдены!")
if __name__ == "__main__":
    main()
