import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, OneToOneFeatureMixin, TransformerMixin
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

class GroupMedianImputer(BaseEstimator, TransformerMixin):
    def __init__(self, groupby_column, target_columns):
        self.groupby_column = groupby_column
        self.target_columns = target_columns
        self.medians_ = None

    def fit(self, X, y=None):
        input_dataframe = pd.DataFrame(X)
        self.medians_ = input_dataframe.groupby(by=self.groupby_column)[self.target_columns].median()

        self.n_features_in_ = input_dataframe.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()

        return self

    def transform(self, X):
        input_dataframe = pd.DataFrame(X).copy()

        for column in self.target_columns:
            mapped_medians = input_dataframe[self.groupby_column].map(self.medians_[column])
            input_dataframe[column] = input_dataframe[column].fillna(mapped_medians)

        return input_dataframe[self.target_columns]

    def get_feature_names_out(self, input_features=None):
            return np.array(self.target_columns)

class GroupModeImputer(BaseEstimator, TransformerMixin):
    def __init__(self, groupby_column, target_columns):
        self.groupby_column = groupby_column
        self.target_columns = target_columns
        self.modes_ = None

    def fit(self, X, y=None):
        input_dataframe = pd.DataFrame(X)
        self.modes_ = input_dataframe.groupby(by=self.groupby_column)[self.target_columns].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)

        self.n_features_in_ = input_dataframe.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()

        return self

    def transform(self, X):
        input_dataframe = pd.DataFrame(X).copy()

        for column in self.target_columns:
            mapped_modes = input_dataframe[self.groupby_column].map(self.modes_[column])
            input_dataframe[column] = input_dataframe[column].fillna(mapped_modes)

        return input_dataframe[self.target_columns]

    def get_feature_names_out(self, input_features=None):
        return np.array(self.target_columns)

class RareCategoryEncoder(OneToOneFeatureMixin, BaseEstimator, TransformerMixin):
    def __init__(self, min_freq=10, fill_value='Inne'):
        self.min_freq = min_freq
        self.fill_value = fill_value
        self.rare_categories_ = None

    def fit(self, X, y=None):
        input_dataframe = pd.DataFrame(X)

        column_name = input_dataframe.columns[0]

        counts = input_dataframe[column_name].value_counts()
        rare_categories = counts[counts <= self.min_freq].index.tolist()

        self.rare_categories_ = rare_categories

        self.n_features_in_ = input_dataframe.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()

        return self

    def transform(self, X):
        input_dataframe = pd.DataFrame(X).copy()
        column_name = input_dataframe.columns[0]

        rare_category_mask = input_dataframe[column_name].isin(self.rare_categories_)
        input_dataframe.loc[rare_category_mask, column_name] = self.fill_value

        return input_dataframe

class InteractionCreator(BaseEstimator, TransformerMixin):

    def __init__(self, new_column_name):
        self.new_column_name = new_column_name

    def fit(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        self.feature_names_in_ = X.columns
        self.n_features_in_ = X.shape[1]

        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=self.feature_names_in_[:X.shape[1]])

        output_dataframe = X.copy()

        first_column = output_dataframe.iloc[:, 0]
        second_column = output_dataframe.iloc[:, 1]

        denominator = second_column.replace(0, 1)
        output_dataframe[self.new_column_name] = first_column / denominator

        return output_dataframe


    def get_feature_names_out(self, input_features=None):
        if input_features is not None:
            return np.array(list(input_features) + [self.new_column_name])
        return np.array(list(self.feature_names_in_) + [self.new_column_name])


class ScaledKNNImputer(BaseEstimator, OneToOneFeatureMixin, TransformerMixin):
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

    def fit(self, X, y=None):
        input_dataframe = pd.DataFrame(X)

        self.n_features_in_ = input_dataframe.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()

        self.scaler_ = StandardScaler()
        scaled_values = self.scaler_.fit_transform(input_dataframe)

        self.imputer_ = KNNImputer(n_neighbors=self.n_neighbors)
        self.imputer_.fit(scaled_values)

        return self

    def transform(self, X):
        input_dataframe = pd.DataFrame(X)

        scaled_values = self.scaler_.transform(input_dataframe)
        imputed_scaled_values = self.imputer_.transform(scaled_values)
        imputed_values = self.scaler_.inverse_transform(imputed_scaled_values)

        return pd.DataFrame(imputed_values, columns=input_dataframe.columns, index=input_dataframe.index)


def remove_outliers_by_group(X, y):
    dataframe_with_target = X.copy()
    dataframe_with_target["cena"] = y

    lower_quantile = dataframe_with_target.groupby(["marka", "wiek_auta"], dropna=False)["cena"].transform(
        "quantile", 0.25
    )
    upper_quantile = dataframe_with_target.groupby(["marka", "wiek_auta"], dropna=False)["cena"].transform(
        "quantile", 0.75
    )
    iqr = upper_quantile - lower_quantile

    mask = (dataframe_with_target["cena"] >= (lower_quantile - 1.5 * iqr)) & (
        dataframe_with_target["cena"] <= (upper_quantile + 1.5 * iqr)
    )

    return X[mask], y[mask]
