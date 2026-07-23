import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, OneToOneFeatureMixin, TransformerMixin

class GroupMedianImputer(BaseEstimator, TransformerMixin):
    def __init__(self, groupby_col, target_cols):
        self.groupby_col = groupby_col
        self.target_cols = target_cols
        self.medians_ = None

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        self.medians_ = X_df.groupby(by=self.groupby_col)[self.target_cols].median()

        self.n_features_in_ = X_df.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()

        return self
    
    def transform(self, X):
        X_df = pd.DataFrame(X).copy()

        for col in self.target_cols:
            dopasowane_mediany = X_df[self.groupby_col].map(self.medians_[col])
            X_df[col] = X_df[col].fillna(dopasowane_mediany)

        return X_df[self.target_cols]

    def get_feature_names_out(self, input_features=None):
            return np.array(self.target_cols)
    
class GroupModeImputer(BaseEstimator, TransformerMixin):
    def __init__(self, groupby_col, target_cols):
        self.groupby_col = groupby_col
        self.target_cols = target_cols
        self.modes_ = None

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        self.modes_ = X_df.groupby(by=self.groupby_col)[self.target_cols].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)

        self.n_features_in_ = X_df.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()

        return self
    
    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        
        for col in self.target_cols:
            dopasowane_mody = X_df[self.groupby_col].map(self.modes_[col])
            X_df[col] = X_df[col].fillna(dopasowane_mody)

        return X_df[self.target_cols]

    def get_feature_names_out(self, input_features=None):
        return np.array(self.target_cols)
    
class RareCategoryEncoder(OneToOneFeatureMixin, BaseEstimator, TransformerMixin):
    def __init__(self, min_freq=10, fill_value='Inne'):
        self.min_freq = min_freq
        self.fill_value = fill_value
        self.valid_categories_ = None

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        
        col_name = X_df.columns[0]
        
        counts = X_df[col_name].value_counts()
        rare_categories = counts[counts <= self.min_freq].index.tolist()
        
        self.valid_categories_ = rare_categories

        self.n_features_in_ = X_df.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = X.columns.to_numpy()
            
        return self
    
    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        col_name = X_df.columns[0]
        
        maska_rzadkich = X_df[col_name].isin(self.valid_categories_)
        X_df.loc[maska_rzadkich, col_name] = self.fill_value
            
        return X_df
    
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
            
        X_out = X.copy()
        
        kol1 = X_out.iloc[:, 0]
        kol2 = X_out.iloc[:, 1]
        
        mianownik = kol2.replace(0, 1)
        X_out[self.new_column_name] = kol1 / mianownik
        
        return X_out
            
        
    def get_feature_names_out(self, input_features=None):
        if input_features is not None:
            return np.array(list(input_features) + [self.new_column_name])
        return np.array(list(self.feature_names_in_) + [self.new_column_name])

   
def usun_odstajace_w_grupach(X, y):
    df_temp = X.copy()
    df_temp["cena"] = y

    q25 = df_temp.groupby(["marka", "wiek_auta"])["cena"].transform(
        "quantile", 0.25
    )
    q75 = df_temp.groupby(["marka", "wiek_auta"])["cena"].transform(
        "quantile", 0.75
    )
    iqr = q75 - q25

    maska = (df_temp["cena"] >= (q25 - 1.5 * iqr)) & (
        df_temp["cena"] <= (q75 + 1.5 * iqr)
    )

    return X[maska], y[maska]