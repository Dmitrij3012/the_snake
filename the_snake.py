from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_OF_SCREEN = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной класс игры."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=CENTER_OF_SCREEN):
        """Инициализатор класса."""
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Метод предназначенный для преопределения в дочерних классах."""
        raise NotImplementedError('Определите draw в дочерних классах.')


class Apple(GameObject):
    """Дочерний класс Apple."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=[],
                 position=CENTER_OF_SCREEN):
        """Инициализатор класса."""
        super().__init__(body_color, position)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=[]):
        """Метод отвечающий за случайное положение яблока."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    # Метод draw класса Apple
    def draw(self):
        """Метод отвечающий за отрисовку яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс Snake."""

    def __init__(self, body_color=SNAKE_COLOR,
                 position=CENTER_OF_SCREEN):
        """Инициализатор класса Snake."""
        super().__init__(body_color, position)
        self.reset()
        self.direction = RIGHT
        self.last = None

    def move(self):
        """Метод отвечающий за обновление позиции змейки."""
        self.get_head_position()
        dx, dy = self.direction
        self.positions.insert(0, ((self.positions[0][0] + dx * GRID_SIZE)
                                  % SCREEN_WIDTH,
                                  (self.positions[0][1] + dy * GRID_SIZE)
                                  % SCREEN_HEIGHT))

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод осуществляет отрисовку змейки."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает начальную позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние
        после столкновения c собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Функция отвечающая за обработку нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция main."""
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.move()
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
