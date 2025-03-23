import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split

def fit_glm(data, formula, family=sm.families.Gaussian()):
    """
    Fit a Generalized Linear Model (GLM) to the provided data.

    Parameters:
    - data: DataFrame containing the data.
    - formula: A string representing the model formula (e.g., 'y ~ x1 + x2').
    - family: The family of the GLM (default is Gaussian).

    Returns:
    - result: The fitted GLM results.
    """
    model = sm.GLM.from_formula(formula, data, family=family)
    result = model.fit()
    return result

def fit_linear_regression(X, y):
    """
    Fit a Linear Regression model.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.

    Returns:
    - model: The fitted Linear Regression model.
    """
    model = LinearRegression()
    model.fit(X, y)
    return model

def fit_logistic_regression(X, y):
    """
    Fit a Logistic Regression model.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.

    Returns:
    - model: The fitted Logistic Regression model.
    """
    model = LogisticRegression()
    model.fit(X, y)
    return model

def fit_decision_tree_regressor(X, y):
    """
    Fit a Decision Tree Regressor model.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.

    Returns:
    - model: The fitted Decision Tree Regressor model.
    """
    model = DecisionTreeRegressor()
    model.fit(X, y)
    return model

def fit_decision_tree_classifier(X, y):
    """
    Fit a Decision Tree Classifier model.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.

    Returns:
    - model: The fitted Decision Tree Classifier model.
    """
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

def fit_svm_classifier(X, y):
    """
    Fit a Support Vector Machine (SVM) Classifier.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.

    Returns:
    - model: The fitted SVM Classifier model.
    """
    model = SVC()
    model.fit(X, y)
    return model

def fit_svm_regressor(X, y):
    """
    Fit a Support Vector Machine (SVM) Regressor.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.

    Returns:
    - model: The fitted SVM Regressor model.
    """
    model = SVR()
    model.fit(X, y)
    return model

def fit_knn_classifier(X, y, n_neighbors=5):
    """
    Fit a K-Nearest Neighbors (KNN) Classifier.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.
    - n_neighbors: Number of neighbors to use (default is 5).

    Returns:
    - model: The fitted KNN Classifier model.
    """
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X, y)
    return model

def fit_knn_regressor(X, y, n_neighbors=5):
    """
    Fit a K-Nearest Neighbors (KNN) Regressor.

    Parameters:
    - X: Features DataFrame.
    - y: Target variable.
    - n_neighbors: Number of neighbors to use (default is 5).

    Returns:
    - model: The fitted KNN Regressor model.
    """
    model = KNeighborsRegressor(n_neighbors=n_neighbors)
    model.fit(X, y)
    return model

# Example usage:
# data = pd.read_csv('your_data.csv')
# X = data[['feature1', 'feature2']]
# y = data['target']
# linear_model = fit_linear_regression(X, y)
# logistic_model = fit_logistic_regression(X, y)
# tree_model = fit_decision_tree_regressor(X, y)
# tree_classifier = fit_decision_tree_classifier(X, y)
# svm_model = fit_svm_classifier(X, y)
# knn_model = fit_knn_regressor(X, y)

# Example usage for different distributions:

# 1. Gaussian (Normal) Distribution
# result_gaussian = fit_glm(data, 'response_variable ~ predictor1 + predictor2', family=sm.families.Gaussian())
# print("Gaussian GLM Summary:")
# print(result_gaussian.summary())

# 2. Binomial Distribution
# result_binomial = fit_glm(data, 'successes + failures ~ predictor1 + predictor2', family=sm.families.Binomial())
# print("Binomial GLM Summary:")
# print(result_binomial.summary())

# 3. Poisson Distribution
# result_poisson = fit_glm(data, 'count_variable ~ predictor1 + predictor2', family=sm.families.Poisson())
# print("Poisson GLM Summary:")
# print(result_poisson.summary())

# 4. Negative Binomial Distribution
# result_negative_binomial = fit_glm(data, 'count_variable ~ predictor1 + predictor2', family=sm.families.NegativeBinomial())
# print("Negative Binomial GLM Summary:")
# print(result_negative_binomial.summary())

# 5. Gamma Distribution
# result_gamma = fit_glm(data, 'response_variable ~ predictor1 + predictor2', family=sm.families.Gamma())
# print("Gamma GLM Summary:")
# print(result_gamma.summary())

# 6. Inverse Gaussian Distribution
# result_inverse_gaussian = fit_glm(data, 'response_variable ~ predictor1 + predictor2', family=sm.families.InverseGaussian())
# print("Inverse Gaussian GLM Summary:")
# print(result_inverse_gaussian.summary())
