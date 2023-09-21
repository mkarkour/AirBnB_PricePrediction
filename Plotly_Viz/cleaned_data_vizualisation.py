import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from raw_data_vizualisation import PlotByCity_Scatter, plot_join

def cleaned_data_correlation(cleaned_data):
    df=cleaned_data
    plt.figure(figsize=(20,10))
    plt.title('Correlation of Attributes', y=1.05, size=19)
    sns.heatmap(df.corr(),cmap='rocket_r',center=True,mask=np.triu(np.ones_like(df.corr(), dtype=bool)))


def plot_by_city(clean_data,parameter) :
    #metro_dist,dist
    PlotByCity_Scatter(clean_data,parameter)
