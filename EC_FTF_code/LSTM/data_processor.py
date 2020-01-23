import math
import numpy as np
import pandas as pd

class DataLoader():
    """A class for loading and transforming data for the lstm model"""

    def __init__(self, filename, split, cols):
        dataframe = pd.read_csv(filename)
        i_split = int(len(dataframe) * split)
        self.data_train = dataframe['value'].values[:i_split]
        self.data_test  = dataframe['value'].values[i_split:]
        self.len_train  = len(self.data_train)
        self.len_test   = len(self.data_test)
        self.len_train_windows = None
    def get_test_data(self, seq_len, normalise):
        '''
        Create x, y test data windows
        Warning: batch method, not generative, make sure you have enough memory to
        load data, otherwise reduce size of the training split.
        '''
        windows = self.data_test[0:seq_len]
        x = []
        y = []
        data_x = []
        data_y = []
        for j in range(6):
            x.append(windows[j * 48:(j + 1) * 48])

        data_x.append(x)
        data_y = windows[6 * 48:7 * 48]
        return data_x,data_y

    def get_multi_train_data(self,seq_len):
        data_x = []
        data_y = []
        i = 0
        while i < self.len_train-seq_len:
            windows = self.data_train[i:i+seq_len]
            x=[]
            y=[]
            for  j in range(6):
                x.append(windows[j*48:(j+1)*48])
                y = windows[6*48:7*48]
            data_x.append(x)
            data_y.append(y)
            i = i+24
        return np.array(data_x), np.array(data_y)

    def get_train_data(self, seq_len, normalise):
        '''
        Create x, y train data windows
        Warning: batch method, not generative, make sure you have enough memory to
        load data, otherwise use generate_training_window() method.
        '''
        data_x = []
        data_y = []
        for i in range(self.len_train - seq_len):
            x, y = self._next_window(i, seq_len, normalise)
            data_x.append(x)
            data_y.append(y)
        return np.array(data_x), np.array(data_y)

    def generate_multi_train_batch(self, seq_len, batch_size):
        i = 0
        while i < (self.len_train - batch_size*12-seq_len):
            x_batch = []
            y_batch = []
            x = []
            y = []
            if i+batch_size*12+seq_len<self.len_train:
                for b in range(batch_size):
                    windows = self.data_train[i:i+seq_len]
                    #print(np.array(windows).shape)
                    x = []
                    y = []
                    for j in range(6):
                        x.append(windows[j*48:(j+1)*48])
                    y = windows[6*48:7*48]
                    x_batch.append(x)
                    y_batch.append(y)
                    #print(np.array(x_batch).shape)
                    i = i+12
                    if i>self.len_train - batch_size*12-seq_len:
                        i = 0
                    else:
                        pass
                yield np.array(x_batch), np.array(y_batch)
            else:
                i = 0


    def generate_train_batch(self, seq_len, batch_size, normalise):
        '''Yield a generator of training data from filename on given list of cols split for train/test'''
        i = 0
        while i < (self.len_train - seq_len):
            x_batch = []
            y_batch = []
            for b in range(batch_size):
                if i >= (self.len_train - seq_len):
                    # stop-condition for a smaller final batch if data doesn't divide evenly
                    yield np.array(x_batch), np.array(y_batch)
                    i = 0
                x, y = self._next_window(i, seq_len, normalise)
                x_batch.append(x)
                y_batch.append(y)
                i += 1
            yield np.array(x_batch), np.array(y_batch)

    def _next_window(self, i, seq_len, normalise):
        '''Generates the next data window from the given index location i'''
        window = self.data_train[i:i+seq_len]
        window = self.normalise_windows(window, single_window=True)[0] if normalise else window
        x = window[:-1]
        y = window[-1, [0]]
        return x, y

    def normalise_windows(self, window_data, single_window=False):
        '''Normalise window with a base value of zero'''
        normalised_data = []
        window_data = [window_data] if single_window else window_data
        for window in window_data:
            normalised_window = []
            for col_i in range(window.shape[1]):
                normalised_col = [((float(p) / float(window[0, col_i])) - 1) for p in window[:, col_i]]
                normalised_window.append(normalised_col)
            normalised_window = np.array(normalised_window).T # reshape and transpose array back into original multidimensional format
            normalised_data.append(normalised_window)
        return np.array(normalised_data)