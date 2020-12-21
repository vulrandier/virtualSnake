from enum import Enum
from random import Random


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Field(Enum):
    FREE = 0
    FOOD = 1
    TAIL = 2


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return 'Postion [%i | %i]' % (self.x, self.y)

    def __add__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x - other.x, self.y - other.y)

    def scalar(self, other) -> int:
        if not isinstance(other, Position):
            return NotImplemented
        return (self.x * other.x) + (self.y * other.y)

    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


class Map:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.area = {}

    def render(self):
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                isInDict = Position(x, y) in self.area.keys()
                field = self.area[Position(x, y)] if Position(x, y) in self.area.keys() else Field.FREE
                if (field == Field.FREE):
                    line += ' '
                elif field == Field.TAIL:
                    line += 'X'
                elif field == Field.FOOD:
                    line += 'O'
            print(line)

    def set_position(self, position: Position, field: Field):
        self.area[position] = field

    def count_free_fields(self) -> int:
        return self.width * self.height - len([1 for position, field in self.area.items() if field != Field.FREE])

    def spawn_food(self, count: int):
        count %= self.count_free_fields()
        rand = Random()
        for i in range(count):
            x = rand.randint(0, self.width)
            y = rand.randint(0, self.height)
            while self.check_position_blocked(Position(x, y)) and self.check_position_for_food(Position(x, y)):
                x = rand.randint(0, self.width)
                y = rand.randint(0, self.height)
            self.set_position(Position(x, y), Field.FOOD)

    def check_position_boundary(self, position: Position) -> bool:
        if position.x >= 0 & position.x < self.width & position.y > 0 & position.y < self.height:
            return True
        return False

    def check_position_blocked(self, position: Position) -> bool:
        if not self.check_position_boundary(position):
            return False
        elif position in self.area.keys():
            return not self.area[position] == Field.TAIL
        return True

    def check_position_for_food(self, position: Position) -> bool:
        if position in self.area.keys():
            if self.area[position] == Field.FOOD:
                return True
        return False


class Snake:
    def __init__(self, map: Map):
        # Stats
        self.isAlive = True
        self.score = 0
        self.turn = 0
        # Direction
        self.deltaX = 0
        self.deltaY = 1
        self.direction = Direction.SOUTH
        # Map
        self.map = map
        # Tails
        self.tails = []
        for i in range(3):
            self.tails.append(Position(i, 0))
            self.map.set_position(self.tails[i], Field.TAIL)

    def turn_left(self):
        if self.direction == Direction.NORTH:
            self.deltaX = -1
            self.deltaY = 0
        elif self.direction == Direction.EAST:
            self.deltaX = 0
            self.deltaY = -1
        elif self.direction == Direction.SOUTH:
            self.deltaX = 1
            self.deltaY = 0
        elif self.direction == Direction.WEST:
            self.deltaX = 0
            self.deltaY = 1

    def turn_right(self):
        if self.direction == Direction.NORTH:
            self.deltaX = 1
            self.deltaY = 0
        elif self.direction == Direction.EAST:
            self.deltaX = 0
            self.deltaY = 1
        elif self.direction == Direction.SOUTH:
            self.deltaX = -1
            self.deltaY = 0
        elif self.direction == Direction.WEST:
            self.deltaX = 0
            self.deltaY = -1

    def check_death(self):
        if self.map.check_position_blocked(self.tails[0]):
            self.isAlive = False

    def check_food(self):
        if self.map.check_position_for_food(self.tails[0]):
            self.grow()

    def grow(self):
        last_tail = self.tails[-1]
        second_last_tail = self.tails[-2]

        delta_x = last_tail.x - second_last_tail.x
        delta_y = last_tail.y - second_last_tail.y

        self.tails.append(Position(last_tail.x + delta_x, last_tail.y + delta_y))
        self.map.set_position(self.tails[-1], Field.TAIL)
        self.score += 1

    def move_forward(self):
        # insert at first
        self.tails.insert(0, Position(self.tails[0].x + self.deltaX, self.tails[0].y + self.deltaY))
        self.map.set_position(self.tails[-1], Field.FREE)
        self.tails = self.tails[:-1]
        self.check_food()
        self.check_death()
        self.map.set_position(self.tails[0], Field.TAIL)
        self.turn += 1

    def __str__(self) -> str:
        result = 'Snake [%i]:\n' % id(self)
        for tail in self.tails:
            result += '\t' + tail.__str__() + '\n'
        return result


def main():
    snake = Snake(Map(10, 10))
    print(snake)
    snake.map.render()
    snake.move_forward()
    snake.grow()
    snake.turn_left()
    snake.move_forward()
    snake.move_forward()
    snake.map.render()
    print(snake)

if __name__ == '__main__':
    main()
