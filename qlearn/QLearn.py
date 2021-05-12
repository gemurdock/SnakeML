import random
from lib.Direction import Direction


def int_array_to_string(arr):
    return ' '.join(str(n) for n in arr)


def generate_all_combinations(array):  # TODO: still needs checking. not generating last combo
    index_array = [0] * len(array)
    combination_array = []
    done = False
    last_pass_done = False
    while not (done and last_pass_done):
        sample = []
        for i in range(len(array)):
            sample.append(array[i][index_array[i]])
        combination_array.append(sample)
        if done:
            last_pass_done = True
            continue
        do_carry = False
        done = True
        for i in range(len(array) - 1, -1, -1):
            if i == len(array) - 1:
                index_array[i] += 1
            elif do_carry:
                index_array[i] += 1
                do_carry = False
            if index_array[i] >= len(array[i]):
                index_array[i] = 0
                do_carry = True
            if index_array[i] < len(array[i]) - 1:
                done = False
    return combination_array


def temporal_difference(max_state_quality, previous_state_quality, reward, discount):
    td = reward + discount * max_state_quality - previous_state_quality
    return td


def new_quality(max_state_quality, previous_state_quality, learn_rate, reward, discount):
    nq = previous_state_quality + learn_rate * temporal_difference(max_state_quality, previous_state_quality,
                                                                     reward, discount)
    return nq


def init_q_table(states_len, actions_len):
    q_table = []
    for _ in range(states_len):
        action_columns = []
        for __ in range(actions_len):
            action_columns.append(0)
        q_table.append(action_columns)
    return q_table


# Parameters:
#   values = String[] or Array of Int[]
def tokenize_values(values, reverse=False):  # TODO: return False, both, need to throw errors
    map_dict = {}
    for i in range(len(values)):
        entry = values[i]
        if isinstance(entry, list) and all([isinstance(x, int) or isinstance(x, Direction) for x in entry]):
            entry = int_array_to_string(entry)
        if not reverse:
            map_dict[entry] = i
        else:
            map_dict[i] = entry
    return map_dict


class QModel:

    def __init__(self, states, actions):
        self.q_table = init_q_table(len(states), len(actions))
        self.state_tokens = tokenize_values(states)
        self.action_tokens = tokenize_values(actions, reverse=True)
        self.state_history = []
        self.action_history = []
        self.learn_rate = 0.9
        self.discount = 0.9
        self.epsilon = 0.2
        self.learn_decay = 0.9
        self.epsilon_decay = 0.85

    def decay(self):
        self.epsilon *= self.epsilon_decay

    def get_table(self):
        return self.q_table

    def get_action(self, state):
        if isinstance(state, list) and all(isinstance(x, int) or isinstance(x, Direction) for x in state):
            state = int_array_to_string(state)
        elif isinstance(state, list) and all(isinstance(x, str) for x in state):
            return False
        encoded_state = self.state_tokens[state]
        row = self.q_table[encoded_state]
        max_value_index = -1
        max_value = -1
        for i in range(len(row)):
            if max_value < row[i]:
                max_value_index = i
                max_value = row[i]
        return self.action_tokens[max_value_index]

    def rand_action(self):
        return self.action_tokens[random.randint(0, len(self.action_tokens) - 1)]

    def setup_training(self, learn_rate, discount, epsilon, learn_decay, epsilon_decay):
        self.learn_rate = learn_rate
        self.discount = discount
        self.epsilon = epsilon
        self.learn_decay = learn_decay
        self.epsilon_decay = epsilon_decay

    def reset_training(self):
        self.state_history = []
        self.action_history = []
        self.learn_rate = 0.9
        self.discount = 0.9
        self.epsilon = 1.0
        self.learn_decay = 0.98
        self.epsilon_decay = 0.98

    def get_train_action(self, state):
        self.state_history.append(state)
        x_rand = random.random()
        if x_rand < self.epsilon:  # TODO: Not working correctly
            next_action = self.action_tokens[random.randint(0, len(self.action_tokens) - 1)]
            print('Random action {}'.format(next_action))
        else:
            next_action = self.get_action(state)
        self.action_history.append(next_action)
        return next_action

    def train(self, state, reward, do_decay=True):
        if len(self.state_history) < 2 or len(self.action_history) < 2:
            return
        print('-- Train --')
        encoded_state = state
        if not isinstance(encoded_state, str):
            encoded_state = int_array_to_string(encoded_state)
        print('State: {} - do_decay={}'.format(state, do_decay))
        max_quality_state = max(self.q_table[self.state_tokens[encoded_state]])
        print('Max State Quality: {}'.format(max_quality_state))
        qti = self.state_tokens[int_array_to_string(self.state_history[len(self.state_history) - 1])]
        qtj = None
        for key, value in self.action_tokens.items():
            if value == self.action_history[len(self.action_history) - 1]:
                qtj = key
                break
        previous_state_quality = self.q_table[qti][qtj]
        print('State history: {}'.format(self.state_history))
        print('Action history: {}'.format(self.action_history))
        print('Previous State Quality: {} with action {}'.format(previous_state_quality, self.action_history[len(self.action_history) - 1]))
        new_state_quality = new_quality(max_quality_state, previous_state_quality,
                                        self.learn_rate, reward, self.discount)
        print('New State Quality: {} ({})'.format(new_state_quality, qti))
        self.q_table[qti][qtj] = new_state_quality
        if do_decay:
            self.learn_rate *= self.learn_decay
            self.epsilon *= self.epsilon_decay
        while len(self.state_history) > 5:
            self.state_history.pop(0)
        while len(self.action_history) > 5:
            self.action_history.pop(0)

    def print_q_table(self):
        print('\nQ - Table')
        for i in range(len(self.q_table)):
            if all(v == 0 for v in self.q_table[i]):
                continue
            state_key = list(self.state_tokens)[i]
            print('{} - {} - {}'.format(self.state_tokens[state_key], state_key, self.q_table[i]))
        print('')
# Agent
# Model
  # States
  # Actions
  # Table
  # Reward table / function - what if we had seperate class that controled rewards? called Enviroment
