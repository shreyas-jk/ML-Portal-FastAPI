from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operation import FileOperation
import os

class KMeansClustering:
    def __init__(self, data):
        self.data = data

    def elbow_plot(self):
        wcss=[]
        for i in range (1, 11):
            kmeans=KMeans(n_clusters=i, init='k-means++', random_state=42)
            kmeans.fit(self.data)
            wcss.append(kmeans.inertia_)
        self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
        return self.kn.knee
    
    def apply_clustering(self, no_clusters):
        self.kmeans = KMeans(n_clusters=no_clusters, init='k-means++', random_state=42)
        self.y_kmeans = self.kmeans.fit_predict(self.data)
        self.data['Cluster'] = self.y_kmeans
        file_op = FileOperation()
        file_op.save_model(self.kmeans, './Clustering_Models/KMeans.pkl')
        return self.data
