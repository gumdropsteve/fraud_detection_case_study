from gradientboost import GradientBoost
from sklearn.ensemble.partial_dependence import plot_partial_dependence, partial_dependence
import pandas as pd
import pickle
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with open('modelg2.p', 'rb') as f:
        model = pickle.load(f)

    feature_names = list(model.data.columns)
    feature_names.remove('fraud')

<<<<<<< HEAD
    features = ['event_delay', 'name_length', 'user_created', 'venue_address', 'avg_price', 'num_payouts']

    fig, axs = plot_partial_dependence(model.m, model.X_train, features, feature_names = feature_names)
    fig.set_title('Partial Dependency Plots')
=======
    features = [[feature_names]]
    fig, axs = plot_partial_dependence(model.m, model.X_train, feature_names, feature_names = feature_names)
>>>>>>> d69dc69fbeb04cd4d5fe3fbc062c341f36d223c9
