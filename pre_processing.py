import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


class Preprocessing:
    def __init__(self, filepath=""):
        self.filepath = filepath

    def read_data_Joensuu(self):
        read = open(self.filepath, "r")
        content = read.readlines()
        data_array = np.empty((len(content), 2)) #Create an empty array to store the lat and lon
        if(len(content) == 0):
            return
        else:
            for line in range(len(content)):
                lat, lon = str(content[line].rstrip()).split(" ")
                content[line] = lat + ","  + lon
                data_array[line, 0] = float(lat)
                data_array[line, 1] = float(lon)
            return data_array
        read.close()

    def standardize_data(self, data):
        data_copy = data.copy()

        rows = data.shape[0]
        cols = data.shape[1]
        for i in range(cols):
            col_mean = np.mean(data[:, i])
            col_std = np.std(data[:, i])

            for j in range(rows):
                data_copy[j, i] = (data[j, i] - col_mean) / col_std

        return data_copy 

    #remove values < -3 and > 3
    def remove_outliers(self, data):
        data_copy = data.copy()
        length = data_copy.shape[0]
        for i in range(length - 1, 0, -1):
            if data[i, 0] < -3.0 or data[i, 0] > 3.0:
                # print(data[i, 0])
                data_copy = np.delete(data_copy, obj=i, axis=0)
                length = data_copy.shape[0]
                continue
            elif data[i, 1] < -3.0 or data[i, 1] > 3.0:
                # print(data[i, 1])
                data_copy = np.delete(data_copy, obj=i, axis=0)
                continue

        return data_copy 

    def normalise_data(self, data):
        data_copy = data.copy()

        rows = data.shape[0]
        cols = data.shape[1]
        for i in range(cols):
            col_max = np.amax(data[:, i])
            col_min = np.amin(data[:, i])

            for j in range(rows):
                data_copy[j, i] = (data[j, i] - col_min) / (col_max - col_min)
        return data_copy

    def centralise(self, data):
        data_copy = data.copy()

        rows = data.shape[0]
        cols = data.shape[1]
        for i in range(cols):
            col_mean= np.mean(data[:, i])

            for j in range(rows):
                data_copy[j, i] = data[j, i] - col_mean

        return data_copy

    def PCA(self, data, n=2):
        pca = PCA(n_components=n)
        pca.fit(data)
        cof = pca.components_
        trasform_data = pca.transform(data)
        return trasform_data
    
    def percentage_of_variance(self, data):
        pca = PCA(n_components=2) #we have two components
        pca.fit(data)
        cof = pca.components_
        plt.bar([1, 2], pca.explained_variance_ratio_, tick_label= [1, 2])
        plt.xlabel("Principal Component")
        plt.ylabel("% Variance Explained")

        plt.show()

    def plot(self, data, x_label, y_label, title):
        fig, ax = plt.subplots()
        # fig.set_size_inches(5, 5)
        ax.plot(data[:,0], data[:, 1], ".", color="green")
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        ax.set_title(title)
        fig.tight_layout()   
        plt.savefig(title + ".jpeg" ,bbox_inches= "tight")
        plt.show()
        return
