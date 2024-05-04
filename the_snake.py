from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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


# Тут опишите все классы игры.
class GameObject:
    """Основной класс игры."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализатор класса."""
        self.body_color = body_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self):
        """Метод предназначенный для преопределения в дочерних классах."""
        pass


class Apple(GameObject):
    """Дочерний класс Apple."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализатор класса."""
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Метод отвечающий за случайное положение яблока."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                         )
        # if проверка чтобы яблоко не попадало на змейку

    # Метод draw класса Apple
    def draw(self):
        """Метод отвечающий за отрисовку яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс Snake."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализатор класса Snake."""
        self.body_color = body_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self):
        """Метод отвечающий за обновление позиции змейки."""
        dx, dy = self.get_head_position()
        if self.direction == LEFT and self.direction != RIGHT:
            self.positions = [(dx - 1 * GRID_SIZE, dy)]
        elif self.direction == RIGHT and self.direction != LEFT:
            self.positions = [(dx + 1 * GRID_SIZE, dy)]
        elif self.direction == UP and self.direction != DOWN:
            self.positions = [(dx, dy - 1 * GRID_SIZE)]
        elif self.direction == DOWN and self.direction != UP:
            self.positions = [(dx, dy + 1 * GRID_SIZE)]

        if self.get_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(1, (dx, dy))
        if len(self.positions) > self.length:
            self.positions.pop(-1)
        else:
            self.positions += self.positions

    # Метод draw класса Snake
    def draw(self):
        """Метод осуществляет отрисовку змейки."""
        for position in self.positions[:-1]:
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

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод оюновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние
        после столкновения c собой.
        """
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = UP | DOWN | LEFT | RIGHT

# Функция обработки действий пользователя


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
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.get_head_position() == snake.positions:
            snake.reset()
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
