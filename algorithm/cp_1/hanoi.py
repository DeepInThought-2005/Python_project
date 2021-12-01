from typing import TypeVar, Generic, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self, name: str) -> None:
        self._container: List[T] = []
        self._name = name
    
    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self):
        return self._container.pop()
    
    def __repr__(self) -> str:
        return repr(self._container)


num_discs: int = 3
tower_a: Stack[int] = Stack('a')
tower_b: Stack[int] = Stack('b')
tower_c: Stack[int] = Stack('c')

for i in range(1, num_discs + 1):
    tower_a.push(i)

def print_move(start: int, end: int):
    print(start._name, "->", end._name)


def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    if n == 1:
        end.push(begin.pop())
        print_move(begin, end)
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)


if __name__ == "__main__":
    hanoi(tower_a, tower_c, tower_b, num_discs)
    print("\nResult: ")
    print(tower_a)
    print(tower_b)
    print(tower_c)