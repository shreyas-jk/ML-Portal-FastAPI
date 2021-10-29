import pickle

class FileOperation():
    def save_model(self, model, model_name):
        with open(model_name, 'wb') as f:
            pickle.dump(model, f)

    def load_model(self, model_name):
        with open(model_name, 'rb') as file:  
            self.model = pickle.load(file)
        return self.model
    