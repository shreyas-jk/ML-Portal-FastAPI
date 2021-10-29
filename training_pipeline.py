from data_preprocessing import PreProcessing
from data_loader import DataLoader
from model_selection import ModelSelection
from data_clustering import KMeansClustering
from file_operation import FileOperation

from logger import Logger
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

class TrainingPipeline:
    def __init__(self):
        self.numerical_columns = None
        self.categorical_columns = None
        self.file_object = open('./Log_Files/training_pipeline.txt', 'a+')
        self.logger = Logger()
            
    def train_model(self, path):
        data_loader = DataLoader()
        self.logger.write_log(self.file_object, 'Loading data file started')
        data = data_loader.load(path)
        self.logger.write_log(self.file_object, 'Data file loaded successfully')

        self.logger.write_log(self.file_object, 'Preprocessing routine started')
        preprocess = PreProcessing(data)
        preprocess.preprocessing_steps()
        self.logger.write_log(self.file_object, 'Preprocessing routine completed successfully')
        
        X = preprocess.X
        
        self.logger.write_log(self.file_object, 'Starting Clustering routine')
        kmeans = KMeansClustering(X)
        no_clusters = kmeans.elbow_plot()
        self.logger.write_log(self.file_object, 'Calculating cluster number using Elbow method')
        X = kmeans.apply_clustering(no_clusters)
        self.logger.write_log(self.file_object, 'Clustering dataset completed successfully')
        X['Output'] = preprocess.y
        list_cluster = X['Cluster'].unique()

        self.logger.write_log(self.file_object, 'Starting cluster based modeling')
        for i in list_cluster:
            cluster_subset = X[X['Cluster'] == i]
            cluster_label = cluster_subset['Output']
            cluster_subset.drop(['Output','Cluster'], axis=1, inplace=True)
            x_train, x_test, y_train, y_test = train_test_split(cluster_subset, cluster_label, test_size=0.20, random_state=0)
            self.logger.write_log(self.file_object, 'Train Test data split successfully for cluster ' + str(i))

            model_selection = ModelSelection()
            self.logger.write_log(self.file_object, 'Starting model selection for cluster ' + str(i))
            best_model, best_model_name, best_model_score = model_selection.get_best_model(x_train, y_train, x_test, y_test)
            self.logger.write_log(self.file_object, 'Best model selected successfully for cluster ' + str(i))

            file_op = FileOperation()
            save_file_name = './Models/' + best_model_name + '_C' + str(i) + '_' + str(best_model_score)[:4] + '.txt'
            file_op.save_model(best_model, save_file_name)
            self.logger.write_log(self.file_object, 'Model saved successfully for cluster ' + str(i))
        self.logger.write_log(self.file_object, 'Training process completed successfully.')
        return
