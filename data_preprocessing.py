from logger import Logger
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn import preprocessing
from imblearn.over_sampling import SMOTE, RandomOverSampler

class PreProcessing():
    def __init__(self, data):
        self.data = data
        self.file_object = open("./Log_Files/data_preprocessing.txt", 'a+')
        self.logger = Logger()

    def impute_numeric(self, columns, strategy='median'):
        imputer = SimpleImputer(missing_values = np.nan, strategy = strategy)
        self.data[columns] = imputer.fit_transform(self.data[columns])

    def impute_categorical(self, columns):
        self.logger.write_log(self.file_object, 'Imputing numerical features')
        for column in columns:
            self.data[column].fillna(self.data[column].mode().values[0], inplace=True)
    
    def load_numerical(self, numerical_columns):
        self.numerical_columns = numerical_columns
    
    def load_categorical(self, categorical_columns):
        self.categorical_columns = categorical_columns

    def get_data(self):
        return self.data

    def encode_categorical(self, strategy='le'):
        if strategy == 'ohe':
            self.logger.write_log(self.file_object, 'Encoder categorical features using LabelEncoder')
            encoded_data = pd.get_dummies(self.data.drop([self.output], axis=1))
            self.data = pd.concat([encoded_data , self.data[self.output]] , axis=1)
        if strategy == 'le':
            self.logger.write_log(self.file_object, 'Encoder categorical features using OneHotEncoder')
            self.data[self.categorical_columns] = self.data[self.categorical_columns].apply(preprocessing.LabelEncoder().fit_transform)

    def set_output(self, output):
        self.output = output
    
    def preprocessing_steps(self):
        self.load_numerical(['Item_Weight', 'Item_Visibility', 'Item_MRP'])
        self.load_categorical(['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier', 'Outlet_Establishment_Year', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type'])
        self.set_output('Item_Outlet_Sales')
        self.impute_numeric(self.numerical_columns, strategy='median')

        self.impute_categorical(self.categorical_columns)
        self.over_sample(strategy='random')
        self.encode_categorical('le')
    
    def test_preprocessing_steps(self):
        self.load_numerical(['Item_Weight', 'Item_Visibility', 'Item_MRP'])
        self.load_categorical(['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier', 'Outlet_Establishment_Year', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type'])
        self.impute_numeric(self.numerical_columns, strategy='median')
        self.impute_categorical(self.categorical_columns)
        self.encode_categorical('le')
    
    @property
    def X(self):
        return self.data.drop(labels=self.output, axis=1)

    @property
    def y(self):
        return self.data[self.output]
    
    def over_sample(self, strategy='random'):
        if strategy == 'smote':
            self.logger.write_log(self.file_object, 'Over sampling dataset using SMOTE')
            smt = SMOTE()
            X_train, y_train = smt.fit_resample(self.X, self.y)
            self.data = pd.concat([X_train, pd.DataFrame(y_train)], axis=1)
        if strategy == 'random':
            self.logger.write_log(self.file_object, 'Over sampling dataset using RandomOverSampler')
            ros = RandomOverSampler()
            X_train, y_train = ros.fit_resample(self.X, self.y)
            self.data = pd.concat([X_train, pd.DataFrame(y_train)], axis=1)

