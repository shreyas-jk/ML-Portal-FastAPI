import pandas as pd

class DataLoader():
    def load(self, path):
        return pd.read_csv(path)
    
    def save(self, data, filename):
        data.to_csv('./'+ filename)