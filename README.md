# Machine Learning Portal

- [Goal](#Goal)
- [Application](#Application)
- [Workflow](#Workflow)
- [Process Design](#Process)
- [Live Project](#Live)

# Goal
A complete end-to-end machine learning portal that covers processes starting from model training to model predicting results using FastAPI. 

# Application
### Main Menu
- Dataset: Set default dataset from the list that will be used for training and building the models.
- Train: Start the training process
- Prediction: Upload test dataset to get predictions.

Save sample test data ([sample_test.csv](https://github.com/shreyas-jk/ML-Portal-FastAPI/blob/main/sample_test.csv)) for testing the prediction module.

### Logger Menu
- Data Preprocessing: Logs generated during preprocessing process.
- Training: Logs generated during training process.
- Prediction: Logs generated during prediction process.

# Workflow
- Import/upload dataset
- Preprocessing
  - Categorical features cleaning
  - Handling missing value (categorical)
  - Handling missing value (numeric)
  - Encoding cateogrical feature
  - Over sampling
  - Clustering
  - Train-Test split
  - Model selection
    - Hyper parameter tuning
  - Saving best model
  - Download prediction results
  
# Process Design <a name = "Process"></a>
![Design](https://github.com/shreyas-jk/ML-API/blob/main/images/flow.png)

# Live Project <a name = "Live"></a>
https://machine-learning-portal.herokuapp.com

# YouTube Demo
[![Watch the video]()](https://www.youtube.com/watch?v=p7jGqMkxRG4)
https://www.youtube.com/watch?v=p7jGqMkxRG4
