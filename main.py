import math
import time
import pygame
from qlearn.FeatureExtractor import extract_features, convert_ai_dir_choice
from qlearn.QLearn import QModel, generate_all_combinations, int_array_to_string
from Grid import Grid
from Snake import Snake
from Food import Food
from lib.GameState import GameState
from lib.Direction import Direction, AIDirectionChoice

IS_HUMAN_PLAYER = False
MAX_EPISODES_TRAIN = 100
WIDTH = 810
HEIGHT = 505
PAD = 5

BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("Comic Sans MS", 30)
text = font.render('%d points' % 0, True, BLACK)

# -- Game Vars --
is_training = not IS_HUMAN_PLAYER
do_train = False
episodes_index = 0
moves_since_score = 0
danger_array = [0, 1]
dir_array = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
food_dir_array = [-1, 0, 1]
q_model = QModel(generate_all_combinations([danger_array, danger_array, danger_array, dir_array,
                                            food_dir_array, food_dir_array]),
                 [AIDirectionChoice.LEFT, AIDirectionChoice.FORWARD, AIDirectionChoice.RIGHT])
player_died = False
player_ate = False
previous_dist = -1.0

state = GameState.RUNNING
last_tick = math.floor(time.time() * 1000)
grid = Grid(0, 100, WIDTH, HEIGHT - 100, 15, 15, 0, 5)
snake = Snake(grid.get_size())
food = Food(grid.get_size(), snake)
player_points = 0
player_direction = Direction.RIGHT

print("Grid size: %s" % (grid.get_size(),))

running = True
while running:
    time_now = math.floor(time.time() * 1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                player_direction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                player_direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                player_direction = Direction.DOWN
            elif event.key == pygame.K_SPACE and state == GameState.FINISHED:
                print('Reset!')
                player_died = False
                player_ate = False
                previous_dist = -1.0
                state = GameState.RUNNING
                last_tick = math.floor(time.time() * 1000)
                snake = Snake(grid.get_size())
                food = Food(grid.get_size(), snake)
                player_points = 0
                player_direction = Direction.RIGHT
                moves_since_score = 0


    # Get state
    # Get next Action
    # Train
    # If i < episodes_max; restart

    if (time_now - last_tick) >= 250 and state == GameState.RUNNING:  # Each tick of the game, do this
        if not IS_HUMAN_PLAYER:
            features = extract_features(player_direction, grid, snake, food)
            feature_index = q_model.state_tokens[int_array_to_string(features)]  # TODO: delete along with prints
            print('\nPre Features: {} ({})'.format(features, feature_index))
            if is_training:
                print('Previous Dir: {}'.format(player_direction))
                player_direction = convert_ai_dir_choice(player_direction, q_model.get_train_action(features))
                print('Next Dir: {}'.format(player_direction))
                moves_since_score += 1
                print('Moves: {}'.format(moves_since_score))
                do_train = True
            else:
                print('Error with is_training')
        else:
            print('Error with IS_HUMAN_PLAYER')

        is_on_map = snake.move(player_direction)
        if not is_on_map and state != GameState.FINISHED:
            state = GameState.FINISHED
            player_died = True
            episodes_index += 1
            q_model.decay()
            print('Player died')
        if snake.get_block(0).intersects(food.get_pos()[0], food.get_pos()[1]):
            food.eat()
            print('Player ate')
            moves_since_score = 0
            player_ate = True
            player_points += 1
            text = font.render('%d points' % player_points, True, (0, 0, 0))
            snake.grow()
            food = Food(grid.get_size(), snake)
        for i in range(1, snake.get_size()):
            head_x, head_y = snake.get_block(0).get_pos()
            if snake.get_block(i).intersects(head_x, head_y) and state != GameState.FINISHED:
                state = GameState.FINISHED
                player_died = True
                episodes_index += 1
                q_model.decay()
                print('Player died')
                break
        last_tick = math.floor(time.time() * 1000)
    elif state == GameState.PAUSED:
        last_tick = math.floor(time.time() * 1000)

    if do_train:
        features = extract_features(player_direction, grid, snake, food)
        print('Train Features: {}'.format(features))
        food_x, food_y = food.get_pos()
        print('Food Pos: {}, {}'.format(food_x, food_y))
        print('Snake Pos: {}, {}'.format(snake.get_block(0).get_pos()[0], snake.get_block(0).get_pos()[1]))
        food_dist = snake.get_block(0).dist(food_x, food_y)
        print('Food dist: {}'.format(food_dist))
        reward = 1
        if player_died:
            reward = -100
            player_died = False
        elif player_ate:
            reward = 10
            player_ate = False
            previous_dist = food_dist = -1
        elif previous_dist < 0:
            reward = 0
        elif food_dist < previous_dist:
            reward = 5
        elif food_dist > previous_dist:
            reward = -5
        print('Reward: {}'.format(reward))

        q_model.train(features, reward, do_decay=False)
        previous_dist = food_dist
        do_train = False

    if episodes_index >= MAX_EPISODES_TRAIN:
        is_training = False
    if moves_since_score > 100 and state != GameState.FINISHED:
        state = GameState.FINISHED
        player_died = True
        episodes_index += 1
        print('At Episode: {} out of {}'.format(episodes_index, MAX_EPISODES_TRAIN))
        q_model.decay()
        q_model.print_q_table()

    screen.fill((255, 255, 255))

    grid.draw(screen)
    snake.draw(screen, grid)
    food.draw(screen, grid)
    screen.blit(text, (WIDTH / 2 - (text.get_size()[0] / 2), 0))

    pygame.display.flip()

pygame.quit()
