import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
import sys


# first get and clean all data needed
def get_data(columns):
    # read in the data
    api_data = pd.read_csv('stage1and2-gatherAndCleanData/nhlAPI/5v5nhl_season_averages.csv')
    other_data = pd.read_csv('stage1and2-gatherAndCleanData/moneypuck/seasonAveragesByTeam.csv')
    
    # remove first 2 columns in other_data as we have those in api_data
    other_data = other_data.drop(columns=['for_avg_shots_on_goal_5on5','for_avg_shots_on_goal_all'])
    

    # make 1 dataframe using the above
    # https://pandas.pydata.org/docs/reference/api/pandas.merge.html
    data = pd.merge(api_data, other_data, on='team')
    # print(data.head())
    
    # Now get all columns we will use for the ML
    data = data[columns]
    # print(data.head())
    # print(data) we have all 32 teams
       
    return data


# Build and compare different clustering models we went over in class
# and from exercise 8 
# While using the minmaxscaler sclaer and PCA
# https://scikit-learn.org/1.5/modules/generated/sklearn.preprocessing.MinMaxScaler.html
# https://scikit-learn.org/dev/modules/generated/sklearn.decomposition.PCA.html

def get_pca(X):
    
    flatten_model = make_pipeline(
        MinMaxScaler(),
        PCA(n_components=2),
        
    )
    X2 = flatten_model.fit_transform(X)
    assert X2.shape == (X.shape[0], 2)
    return X2


def kmeans_model(X_data):

    # KMeans: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
    kmeans_model = make_pipeline(
        MinMaxScaler(),
        KMeans(n_clusters=5),
    )
    
    kmeans_model.fit(X_data)
    return kmeans_model.fit_predict(X_data)


def agglomerative_model(X_data):
    
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
    agglo_model = make_pipeline(
        MinMaxScaler(),
        AgglomerativeClustering(n_clusters=5),
    )
    
    agglo_model.fit(X_data)
    return agglo_model.fit_predict(X_data)

def affinity_model(X_data):
     
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AffinityPropagation.html
    affinity_model = make_pipeline(
        MinMaxScaler(),
        AffinityPropagation(),
    )
    
    affinity_model.fit(X_data)
    return affinity_model.fit_predict(X_data) 


# Create function to visualize each model clusters
# https://medium.com/@marvelouskgc/three-ways-to-add-labels-to-each-data-point-in-a-scatter-plot-in-python-matplotlib-eugene-tsai-42e4094dc07e
def visualize_clusters(X2, clusters, team_name, points, model_name, dataset_id):
    plt.figure(figsize=(14, 10))
    plt.scatter(X2[:, 0], X2[:, 1], c=clusters, cmap='Set1', edgecolor='k', s=100)
    
    for i, team in enumerate(team_name):
        plt.annotate(
            team,
            (X2[i, 0], X2[i, 1]),
            xytext=(5, 10),
            textcoords="offset points",
        )
    for i, point in enumerate(points):
        plt.annotate(
            f"({point})",
            (X2[i, 0], X2[i, 1]),
            xytext=(25, 10),
            textcoords="offset points",
        )
    
    plt.title(f"Clusters Visualization using {model_name} for {dataset_id.replace('_', ' ')}")
    plt.xlabel("PCA Component 1", fontsize=12)
    plt.ylabel("PCA Component 2", fontsize=12)
    plt.savefig(f"stage4-results/{model_name}_clusters_data_{dataset_id}.png")
    plt.close()

def main():
    datasets = {
        "r_>=_0.0": ['team', 'avg_shots_on_goal', 'corsi', 'fenwick', 'corsi_%', 'fenwick_%', 
               'o_zone_faceoff_%', 'd_zone_faceoff_%', 'n_zone_faceoff_%', 'for_avg_defender_shots', 
               'for_avg_long_shots', 'for_avg_WRIST_shots', 'for_avg_SLAP_shots', 'for_avg_SNAP_shots',
               'for_avg_BACKHAND_shots', 'for_avg_TIP_shots', 'for_avg_rebound_shots'],
        "r_>=_0.2": ['team', 'avg_shots_on_goal', 'corsi', 'fenwick', 'corsi_%', 'fenwick_%', 
               'for_avg_defender_shots', 'for_avg_long_shots', 'for_avg_WRIST_shots', 'for_avg_SLAP_shots', 
               'for_avg_SNAP_shots', 'for_avg_BACKHAND_shots', 'for_avg_TIP_shots', 'for_avg_rebound_shots'],
        "r_>=_0.4": ['team', 'avg_shots_on_goal', 'corsi', 'fenwick', 'corsi_%', 'fenwick_%', 
               'for_avg_defender_shots', 'for_avg_long_shots', 'for_avg_WRIST_shots', 'for_avg_rebound_shots'],
        "r_>=_0.6": ['team', 'avg_shots_on_goal', 'corsi', 'fenwick', 'fenwick_%', 
               'for_avg_defender_shots', 'for_avg_long_shots', 'for_avg_WRIST_shots'],
    }
    
    season_points = pd.read_csv('stage1and2-gatherAndCleanData/nhlAPI/season_team_points.csv')
    
    for dataset_id, columns in datasets.items():
        data = get_data(columns)
        X_data = data.iloc[:, 1:]
        y = data.iloc[:, 0]
        X2 = get_pca(X_data)
        
        # run each model with pca
        kmeans_clusters_PCA = kmeans_model(X2)
        agglomerative_clusters_PCA = agglomerative_model(X2)
        affinity_clusters_PCA = affinity_model(X2)
        
        # Create a dataframe to compare all models
        # and visualize the clusters 
        df = pd.DataFrame({
            'team': y,
            'kmeans_PCA': kmeans_clusters_PCA,
            'agglomerative_PCA': agglomerative_clusters_PCA,
            'affinity_PCA': affinity_clusters_PCA,
        })

        # Read in season point data to compare with clusters
        season_points = pd.read_csv('stage1and2-gatherAndCleanData/nhlAPI/season_team_points.csv')
    
        # Merge the season points with the clusters
        end_data = pd.merge(season_points, df, on='team')
        # print(end_data)
        
        # Visualize the clusters and draw conclusions
        points = end_data['points']

        # Visualize clusters
        visualize_clusters(X2, kmeans_clusters_PCA, y, points, 'KMeans', dataset_id)
        visualize_clusters(X2, agglomerative_clusters_PCA, y, points, 'Agglomerative', dataset_id)
        visualize_clusters(X2, affinity_clusters_PCA, y, points, 'Affinity', dataset_id)
        
        # group by each cluster and get the average points, print out team names in each cluster as well
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html
        # https://stackoverflow.com/questions/22219004/how-to-group-dataframe-rows-into-list-in-pandas-groupby
        # from ^^^^ link df.groupby('a').agg({'b':lambda x: list(x)})
        # from https://stackoverflow.com/questions/22219004/how-to-group-dataframe-rows-into-list-in-pandas-groupby/55839464#55839464
        # can use function, str, list, or dict to aggregate data
        # using list here to get a list of all teams in each cluster

        print(f"Dataset {dataset_id}:")
        for model_name, cluster_col in [("KMeans", 'kmeans_PCA'), 
                                        ("Agglomerative", 'agglomerative_PCA'), 
                                        ("Affinity", 'affinity_PCA')]:
            group = end_data.groupby(cluster_col).agg({'points': 'mean', 'team': list})
            group = group.sort_values('points', ascending=False)
            print(f"{model_name} Clusters:")
            print(group)
            print("\n")


if __name__ == "__main__":
    main()
    
