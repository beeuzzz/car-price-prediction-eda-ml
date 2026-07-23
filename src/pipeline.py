import numpy as np
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, StandardScaler
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn import FunctionSampler

from src.transformers import (
    GroupMedianImputer,
    GroupModeImputer,
    RareCategoryEncoder,
    InteractionCreator,
    ScaledKNNImputer,
    remove_outliers_by_group
)

def build_preprocessing_pipeline():
    outlier_removal_step = FunctionSampler(func=remove_outliers_by_group, validate=False)

    brand_imputation_preprocessor = ColumnTransformer(
    transformers=[
        ('imputacja_marki',
            SimpleImputer(strategy='constant', fill_value='Inna marka'),
            ['marka'])
    ],
    remainder='passthrough',
    verbose_feature_names_out=False)

    imputation_preprocessor = ColumnTransformer(
        transformers=[
            ('group_median_imputer',
                GroupMedianImputer(groupby_column='marka', target_columns=['pojemnosc_silnika', 'moc_silnika']),
                ['marka', 'pojemnosc_silnika', 'moc_silnika']),

            ('group_mode_imputer',
                GroupModeImputer(groupby_column='marka', target_columns=['naped', 'nadwozie', 'skrzynia_biegow']),
                ['marka', 'naped', 'nadwozie', 'skrzynia_biegow']),

            ('simple_imputer_cat',
                SimpleImputer(strategy='most_frequent'),
                ['wojewodztwo', 'paliwo', 'kolor', 'liczba_drzwi',
                'typ_sprzedawcy', 'serwis_aso', 'importowany', 'skorzana_tapicerka',
                'dach_panoramiczny', 'swiatla_led']),

            ('simple_imputer_num',
                SimpleImputer(strategy='median'),
                ['ilosc_wyposazenia']),

            ('knn_imputer',
                ScaledKNNImputer(n_neighbors=5),
                ['wiek_auta', 'przebieg']),

            ('zachowaj_marke', 'passthrough', ['marka'])
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    rare_category_preprocessor = ColumnTransformer(
        transformers=[
            ('rare_category_encoder_marka',
                RareCategoryEncoder(min_freq=10, fill_value='Inna marka'),
                ['marka']),

            ('rare_category_encoder_kolor',
                RareCategoryEncoder(min_freq=15, fill_value='Inny kolor'),
                ['kolor'])
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    # 4. Feature Engineering
    feature_engineering_preprocessor = ColumnTransformer(
        transformers=[
            ('engineering1',
                InteractionCreator(new_column_name='przebieg_do_wieku_auta'),
                ['przebieg', 'wiek_auta']),
            ('engineering2',
                InteractionCreator(new_column_name='moc_silnika_do_pojemnosc_silnika'),
                ['moc_silnika', 'pojemnosc_silnika'])
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    # 5. Skalowanie
    scaling_preprocessor = ColumnTransformer(
        transformers=[
            ('skalowanie',
                StandardScaler(),
                make_column_selector(dtype_include=np.number))
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    # 6. Kodowanie
    encoding_preprocessor = ColumnTransformer(
        transformers=[
            ('one_hot_encoding',
                OneHotEncoder(
                    sparse_output=False,
                    handle_unknown='ignore',
                    drop='if_binary'
                ),
                make_column_selector(dtype_include='object'))
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    # 7. Finalny Pipeline
    preprocessing_pipeline = ImbPipeline([
        ('czyszczenie_outlierow', outlier_removal_step),
        ('imputacja_marki', brand_imputation_preprocessor),
        ('imputacja', imputation_preprocessor),
        ('rzadkie_kategorie', rare_category_preprocessor),
        ('feature_engineering', feature_engineering_preprocessor),
        ('skalowanie', scaling_preprocessor),
        ('kodowanie', encoding_preprocessor),
    ]).set_output(transform="pandas")

    return preprocessing_pipeline
