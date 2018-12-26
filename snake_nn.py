from snake import Snake
import numpy as np
import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression

class SnakeNN:
    def __init__(self,load_from_file = False):
        self.training_data = []
        self.create_model()
        
        if not load_from_file:
            self.get_train_data()
            self.train_model()
        else:
            self.brain.load('snake.model')

    def create_model(self):
        network = input_data(shape=[None, 5, 1], name='input')
        network = fully_connected(network, 25, activation='relu')
        network = fully_connected(network, 50, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=0.001, loss='mean_square', name='target')
        self.brain = tflearn.DNN(network, tensorboard_dir='log')

    def train_model(self):
        X = np.array([i[0] for i in self.training_data]).reshape(-1, 5, 1)
        y = np.array([i[1] for i in self.training_data]).reshape(-1,1)
        print(y)
        self.brain.fit(X,y, n_epoch = 3, shuffle = True, run_id = 'snake.model')
        self.brain.save('snake.model')

    def get_train_data(self):
        for i in range(0,10000):
            train_game = Snake(autoplay=True,gui=False)
            #print(train_game.play_game())
            self.training_data = self.training_data + train_game.play_game()
            print(i)
            print(len(self.training_data))

if __name__ == "__main__":
    gameNN = SnakeNN(load_from_file = True)
    game = Snake(autoplay=True,gui=True, brain = gameNN.brain)
    game.play_game()

