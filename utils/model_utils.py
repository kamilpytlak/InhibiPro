import json
from os.path import exists
from typing import List, Dict

import joblib
import pandas as pd
from rdkit.Chem import Draw

import streamlit as st
from tensorflow import keras


def similar_molecules_to_df(similar_molecules: List[Dict]) -> pd.DataFrame:
    column_names = ['Molecule ChEMBL ID', 'Name', 'Similarity [in %]', 'SMILES']
    similar_molecules_df = pd.DataFrame(similar_molecules)

    if similar_molecules_df.empty:
        return pd.DataFrame(columns=column_names)

    similar_molecules_df.columns = column_names
    similar_molecules_df['Similarity [in %]'] = (similar_molecules_df['Similarity [in %]']
                                                 .astype(float)
                                                 .round(2)
                                                 )

    return similar_molecules_df


@st.cache_data
def load_selected_features(path: str) -> list:
    with open(path) as f:
        selected_features = json.load(f)
    return selected_features


@st.cache_resource
def load_model(model_path: str):
    if exists(model_path):
        return keras.models.load_model(model_path)
    else:
        return joblib.load(model_path + '.joblib')


def preprocess_descriptors(descriptors_df, preprocessor_imputer, selected_features):
    descriptors_df = preprocessor_imputer.transform(descriptors_df)
    descriptors_df = descriptors_df[selected_features]
    return descriptors_df


def preprocess_fingerprints(fingerprints_df, selected_features):
    return fingerprints_df[selected_features]


def process_molecule(smiles, target, molecule, model, features):
    predicted_pic50 = model.predict(features)[0]
    molecule_img = Draw.MolToImage(molecule.mol)

    st.markdown(f"SMILES inputed: {smiles}")
    with st.expander('Display molecule'):
        st.image(molecule_img)

    st.markdown(f"Predicted bioactivity value: {str(predicted_pic50.round(2))}.")

    molecule_weight = molecule.calculate_molecular_weight()
    inhibition_dose = calculate_inhibition_dose(molecule_weight, predicted_pic50)

    st.markdown(
        f"The mass of the molecule required to inhibit \"{target}\" by 50%: {inhibition_dose} mg."
    )

    st.markdown("Similar molecules to the given SMILES:")

    try:
        similar_molecules_df = similar_molecules_to_df(molecule.find_similar_molecules())
    except Exception as e:
        st.write('The connection to the ChEMBL database has not been established.'
                 ' Similar molecules cannot be generated.')
    else:
        st.dataframe(similar_molecules_df)


def calculate_inhibition_dose(molecular_weight: float, pic50: float) -> float:
    return ((molecular_weight * 10 ** -pic50) * 1000).round(5)
