from os import listdir

import joblib
import pandas as pd
import streamlit as st

from utils.model_utils import load_selected_features, load_model, preprocess_descriptors, \
    preprocess_fingerprints, process_molecule
from utils.molecule_utils import Molecule

# Constants
TARGET_NAMES = sorted(listdir('models'), key=str.casefold)
FING_COLUMNS = [f"Morgan_{i}" for i in range(1, 2049)]

# Streamlit app configuration
st.set_page_config(
    page_title='Single pIC50 Predictor',
    page_icon='🧪'
)

st.title("Single pIC50 Predictor")

# Input: Select protein target
target_input = st.selectbox(label='Target human protein', options=TARGET_NAMES)


def load_required_files(target_input: str, method: str):
    """Load the required model, preprocessor/imputer, and selected features."""
    base_path = f"models/{target_input}/{method.lower()}"

    if method == 'Descriptors':
        preprocessor_imputer_path = f"{base_path}/preprocessor_imputer.joblib"
        preprocessor_imputer = joblib.load(preprocessor_imputer_path).set_output(transform='pandas')
    else:
        preprocessor_imputer = None  # Fingerprints may not need preprocessor

    selected_features_path = f"{base_path}/selected_features.json"
    model_path = f"{base_path}/model"

    selected_features = load_selected_features(selected_features_path)
    model = load_model(model_path)

    return preprocessor_imputer, selected_features, model


def handle_prediction(smiles_input: str, target_input: str, molecule: Molecule, method: str) -> None:
    """Handle the prediction logic based on method (Descriptors/Fingerprints)."""
    try:
        preprocessor_imputer, selected_features, model = load_required_files(target_input, method)

        if method == 'Descriptors':
            descriptors_df = pd.DataFrame(molecule.generate_descriptors(), index=[0])
            descriptors_df = preprocess_descriptors(descriptors_df, preprocessor_imputer, selected_features)
            process_molecule(smiles_input, target_input, molecule, model, descriptors_df)

        elif method == 'Fingerprints':
            fingerprints_df = pd.DataFrame(molecule.generate_fingerprints(), index=[0])
            fingerprints_df = preprocess_fingerprints(fingerprints_df, selected_features)
            process_molecule(smiles_input, target_input, molecule, model, fingerprints_df)

    except FileNotFoundError as e:
        st.error(f"Model files for {method} not found: {e}", icon="🚨")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}", icon="🚨")


# Check if a target was selected
if target_input:
    # Input: Choose between Descriptors or Fingerprints
    desc_fing_options = [dfo.title() for dfo in listdir(f"models/{target_input}")]
    desc_fing_input = st.selectbox(label='Predictions based on descriptors or Morgan fingerprints?',
                                   options=desc_fing_options)

    # Input: Enter SMILES
    smiles_input = st.text_input(label='SMILES', max_chars=5000)

    # On Predict button click
    if st.button(label='Predict pIC50'):
        if not smiles_input:
            st.error('No SMILES was entered!', icon="🚨")
        else:
            molecule = Molecule(smiles_input)

            if not molecule.is_valid_smiles():
                st.error('Incorrect SMILES was entered! Please refer to: '
                         'https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system#Description',
                         icon="🚨")
            else:
                handle_prediction(smiles_input, target_input, molecule, desc_fing_input)
