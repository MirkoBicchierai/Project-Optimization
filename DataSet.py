import numpy as np
from sklearn.datasets import load_svmlight_file


class DataSet:
    def __init__(self, percentage_split):
        self.percentage_split = percentage_split
        self.labels_train = []
        self.labels_test = []
        self.data_train = []
        self.data_test = []
        self.name = ""

    def load_data(self, path, name):
        self.name = name
        data = load_svmlight_file(path)
        tmp_x = data[0].toarray()
        tmp_y = data[1]

        indices = np.arange(len(tmp_x))
        np.random.shuffle(indices)
        tmp_x = tmp_x[indices, :]
        tmp_y = tmp_y[indices]

        ones_column = np.ones((tmp_x.shape[0], 1))
        tmp_x = np.hstack((tmp_x, ones_column))

        split_index = int(0.8 * len(tmp_x))
        self.labels_train = tmp_y[:split_index]
        self.labels_test = tmp_y[split_index:]
        self.data_train = tmp_x[:split_index]
        self.data_test = tmp_x[split_index:]

    def fix(self, numer):
        self.labels_train[self.labels_train == numer] = -1
        self.labels_test[self.labels_test == numer] = -1

    # This two function is only for scipy to minimize with LBFGS-B
    def loss_function(self, w):
        lamda = 1 / self.data_train.shape[0]
        reg_term = lamda / 2 * np.linalg.norm(w) ** 2
        loss_term = np.mean(np.logaddexp(0, - self.labels_train * np.dot(self.data_train, w)))
        total_value = reg_term + loss_term
        return total_value

    def loss_gradient(self, w):
        lamda = 1 / self.data_train.shape[0]
        n = len(self.data_train)
        reg_gradient = lamda * w
        logistic_gradient = np.zeros_like(w)
        for i in range(n):
            exponent = self.labels_train[i] * np.dot(self.data_train[i], w)
            logistic_gradient += - self.labels_train[i] * self.data_train[i] / (1 + np.exp(exponent))

        gradient = reg_gradient + logistic_gradient / n
        return gradient
