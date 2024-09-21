from os import listdir
from typing import List

import joblib
import pandas as pd
import streamlit as st

from utils.model_utils import load_selected_features, load_model, preprocess_descriptors, preprocess_fingerprints
from utils.molecule_utils import Molecule

# Constants
TARGET_NAMES: List[str] = sorted(listdir('models'), key=str.casefold)
FING_COLUMNS: List[str] = [f"Morgan_{i}" for i in range(1, 2049)]

# Streamlit App Configuration
st.set_page_config(
    page_title='Multiple pIC50 Predictor',
    page_icon='💊'
)

st.title("Multiple pIC50 Predictor")


# Functions
def load_and_validate_smiles(file) -> [None, pd.DataFrame]:
    """Load and validate the SMILES from the uploaded file."""
    smiles_df = pd.read_csv(file)
    if 'SMILES' not in smiles_df.columns:
        st.error('There is no "SMILES" column in the loaded data! Please correct the column name to "SMILES".',
                 icon="🚨")
        return None
    return smiles_df


def validate_molecules(smiles_df: pd.DataFrame) -> [None, pd.Series]:
    """Validate all SMILES and return a series of valid molecules."""
    molecules = smiles_df['SMILES'].apply(Molecule)
    valid_molecules = molecules.apply(lambda molecule: molecule.is_valid_smiles())
    if not valid_molecules.all():
        st.error('At least one SMILES is incorrect! Ensure SMILES notation is consistent.', icon="🚨")
        return None
    return molecules


def predict_descriptors(target_input: str, molecules: pd.Series, smiles_df: pd.DataFrame) -> None:
    """Predict pIC50 using descriptors."""
    preprocessor_imputer_path = f"models/{target_input}/descriptors/preprocessor_imputer.joblib"
    selected_features_path = f"models/{target_input}/descriptors/selected_features.json"
    model_path = f"models/{target_input}/descriptors/model"

    preprocessor_imputer = joblib.load(preprocessor_imputer_path).set_output(transform='pandas')
    selected_features = load_selected_features(selected_features_path)
    model = load_model(model_path)

    descriptors_df = pd.DataFrame.from_records(
        molecules.apply(lambda molecule: molecule.generate_descriptors())
    )
    descriptors_df = preprocess_descriptors(descriptors_df, preprocessor_imputer, selected_features)

    predicted_pic50 = model.predict(descriptors_df).round(2)
    smiles_df['Predicted pIC50'] = predicted_pic50

    st.success('pIC50 prediction successfully completed!', icon="✅")
    st.dataframe(smiles_df)


def predict_fingerprints(target_input: str, molecules: pd.Series, smiles_df: pd.DataFrame) -> None:
    """Predict pIC50 using Morgan fingerprints."""
    selected_features_path = f"models/{target_input}/fingerprints/selected_features.json"
    model_path = f"models/{target_input}/fingerprints/model"

    selected_features = load_selected_features(selected_features_path)
    model = load_model(model_path)

    fingerprints_df = pd.DataFrame.from_records(
        molecules.apply(lambda molecule: molecule.generate_fingerprints())
    )
    fingerprints_df = preprocess_fingerprints(fingerprints_df, selected_features)

    predicted_pic50 = model.predict(fingerprints_df).round(2)
    smiles_df['Predicted pIC50'] = predicted_pic50

    st.success('SMILES prediction successfully completed!', icon="✅")
    st.dataframe(smiles_df.style.highlight_max(subset='Predicted pIC50'))


# User Inputs
target_input = st.selectbox(label='Target human protein', options=TARGET_NAMES)

if target_input:
    desc_fing_options = [dfo.title() for dfo in listdir(f"models/{target_input}")]
    desc_fing_input = st.selectbox(label='Predictions based on descriptors or Morgan fingerprints?',
                                   options=desc_fing_options)
    file_upload = st.file_uploader(label='Choose a file', type=['csv'])

    if st.button(label='Predict pIC50'):
        if not file_upload:
            st.error('No file selected!', icon="🚨")
        else:
            smiles_df = load_and_validate_smiles(file_upload)
            if smiles_df is not None:
                molecules = validate_molecules(smiles_df)
                if molecules is not None:
                    if desc_fing_input == 'Descriptors':
                        predict_descriptors(target_input, molecules, smiles_df)
                    elif desc_fing_input == 'Fingerprints':
                        predict_fingerprints(target_input, molecules, smiles_df)
