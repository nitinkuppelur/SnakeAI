from snake import Snake
import numpy as np
import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
import csv
import progressbar
from random import randint

dim_input_layer = 5

class SnakeNN:
    def __init__(self,load_from_file = False, trian_model = False, save_training_data_to_file=False):
        self.training_data = []      
        if load_from_file:
            self.create_model()
            self.brain.load('snake.model')
        if trian_model:
            self.get_train_data(save_training_data_to_file)
            self.create_model()
            self.train_model()

    def create_model(self):
        network = input_data(shape=[None, dim_input_layer, 1], name='input')
        network = fully_connected(network, 25, activation='relu')
        network = fully_connected(network, 50, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=1e-2, loss='mean_square', name='target')
        self.brain = tflearn.DNN(network, tensorboard_dir='log',tensorboard_verbose=3)

    def train_model(self):
        X = np.array([i[0] for i in self.training_data]).reshape(-1, dim_input_layer, 1)
        y = np.array([i[1] for i in self.training_data]).reshape(-1,1)
        #print(y)
        self.brain.fit(X,y, n_epoch = 3, shuffle = True, run_id = 'snake1.model')
        self.brain.save('snake.model')

    def get_train_data(self,save_training_data_to_file=False):
        game_to_be_played = 10000
        bar = progressbar.ProgressBar(maxval=game_to_be_played, \
                widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for i in range(0,game_to_be_played):
            train_game = Snake(autoplay=True,gui=False, snake_len = randint(2,10))
            #print(train_game.play_game())
            self.training_data = self.training_data + train_game.play_game()
            #print(np.matrix(self.training_data))
            bar.update(i+1)
        print(len(self.training_data))
        bar.finish()
        if save_training_data_to_file:
            with open("training_data.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerows(self.training_data)

if __name__ == "__main__":
    gameNN = SnakeNN(load_from_file = True, trian_model = False, save_training_data_to_file = False)
    for i in range(0,10):
        print(i)
        game = Snake(autoplay=True,gui=True, brain = gameNN.brain, snake_len = randint(2,10))
        game.play_game()
        print(game.len)

