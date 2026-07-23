import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.compose import TransformedTargetRegressor

MIN_CENA = 10000
MAX_CENA = 400000
MIN_PRZEBIEG = 5000
MAX_WIEK_AUTA = 25
WYKLUCZONE_PALIWA = ['Elektryczny', 'Benzyna+CNG', 'Etanol']
WYKLUCZONE_KRAJE_POCHODZENIA = ['USA']

KOLUMNY_NUMERYCZNE = [
    'wiek_auta',
    'pojemnosc_silnika',
    'przebieg',
    'moc_silnika',
    'ilosc_wyposazenia'
]
KOLUMNY_KATEGORYCZNE_PODSTAWOWE = [
    'marka', 
    'skrzynia_biegow', 
    'paliwo', 
    'naped', 
    'wojewodztwo', 
    'nadwozie', 
    'kolor', 
    'typ_sprzedawcy', 
    'liczba_drzwi'
]
KOLUMNY_KATEGORYCZNE_WYPOSAZENIE = [
    'skorzana_tapicerka', 
    'importowany', 
    'serwis_aso', 
    'dach_panoramiczny', 
    'swiatla_led', 
    'pierwszy_wlasciciel', 
    'klimatyzacja_automatyczna', 
    'kamera_cofania', 
    'podgrzewane_fotele', 
    'tempomat', 
    'aktywny_tempomat', 
    'czytanie_znakow', 
    'ladowarka_indukcyjna', 
    'swiatla_tylne_led', 
    'android_auto'
]

RANDOM_STATE = 25

PARAM_GRID = {
    'XGBoost': {
        'model': TransformedTargetRegressor(
            regressor=XGBRegressor(random_state=RANDOM_STATE), 
            func=np.log1p, 
            inverse_func=np.expm1
        ),
        'parametry': {
            'Model__regressor__n_estimators': [100, 200, 300],
            'Model__regressor__learning_rate': [0.02, 0.05, 0.1],
            'Model__regressor__max_depth': [3, 6, 7],
            'Model__regressor__min_child_weight': [1, 3, 5],
            'Model__regressor__subsample': [0.7, 0.85, 1.0],
            'Model__regressor__colsample_bytree': [0.5, 0.6, 0.8]
        }
    },
    'RandomForest': {
        'model': TransformedTargetRegressor(
            regressor=RandomForestRegressor(random_state=RANDOM_STATE), 
            func=np.log1p, 
            inverse_func=np.expm1
        ),
        'parametry': {
            'Model__regressor__n_estimators': [200, 300, 400],
            'Model__regressor__max_depth': [10, 15, None],
            'Model__regressor__min_samples_split': [2, 5, 7],
            'Model__regressor__min_samples_leaf': [1, 2, 4],
            'Model__regressor__max_features': ['sqrt', 'log2', None]
        }
    },
    'LinearRegression': {
        'model': TransformedTargetRegressor(
            regressor=LinearRegression(), 
            func=np.log1p, 
            inverse_func=np.expm1
        ),
        'parametry': {
            'Model__regressor__fit_intercept': [True, False],
            'Model__regressor__positive': [False, True]
        }
    },
}

XGBOOST_BEST_PARAMS = {
    'n_estimators': 300,
    'learning_rate': 0.05,
    'max_depth': 6,
    'min_child_weight': 3,
    'subsample': 0.85,
    'colsample_bytree': 0.6
}


GLOWNY_MODEL = TransformedTargetRegressor(
    regressor=XGBRegressor(**XGBOOST_BEST_PARAMS, random_state=RANDOM_STATE),
    func=np.log1p,
    inverse_func=np.expm1
)