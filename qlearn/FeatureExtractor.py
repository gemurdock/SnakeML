from lib.Direction import Direction, AIDirectionChoice


def wrapped_array(array, start_index, amount):
    current_index = start_index
    array_result = []
    for _ in range(amount):
        array_result.append(array[current_index])
        current_index += 1
        if current_index >= len(array):
            current_index = 0
    return array_result


def convert_ai_dir_choice(snake_dir, choice):
    dir_array = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    index = dir_array.index(snake_dir)
    if choice == AIDirectionChoice.LEFT:
        index -= 1
        if index < 0:
            index += len(dir_array)
    elif choice == AIDirectionChoice.RIGHT:
        index += 1
        if index >= len(dir_array):
            index -= len(dir_array)
    return dir_array[index]


def is_block_in_danger(pos, grid, snake):
    if not 0 <= pos[0] < grid.get_size()[0] or not 0 <= pos[1] < grid.get_size()[1]:
        return 1
    for i in range(snake.get_size()):
        block = snake.get_block(i)
        if block.intersects(pos[0], pos[1]):
            return 1
    return 0

def xy_val_dir(target, pos):
    if target < pos:
        return 1
    elif target > pos:
        return -1
    else:
        return 0


def extract_features(player_direction, grid, snake, food):
    head_pos = snake.get_block(0).get_pos()
    features = [
        is_block_in_danger((head_pos[0], head_pos[1] - 1), grid, snake),
        is_block_in_danger((head_pos[0] + 1, head_pos[1]), grid, snake),
        is_block_in_danger((head_pos[0], head_pos[1] + 1), grid, snake),
        is_block_in_danger((head_pos[0] - 1, head_pos[1]), grid, snake)
    ]
    if player_direction == Direction.UP:
        features = wrapped_array(features, 3, 3)
    elif player_direction == Direction.RIGHT:
        features = wrapped_array(features, 0, 3)
    elif player_direction == Direction.DOWN:
        features = wrapped_array(features, 1, 3)
    elif player_direction == Direction.LEFT:
        features = wrapped_array(features, 2, 3)
    else:
        raise Exception('FeatureExtractor.extract_features() does not account for direction: {}'
                        .format(player_direction))

    features.append(player_direction)
    features.append(xy_val_dir(food.get_pos()[0], head_pos[0]))
    features.append(xy_val_dir(food.get_pos()[1], head_pos[1]))

    return features
