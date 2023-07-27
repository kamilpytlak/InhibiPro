from os import listdir

import joblib
import pandas as pd
import streamlit as st

from utils.model_utils import load_selected_features, load_model, preprocess_descriptors,\
    preprocess_fingerprints, process_molecule
from utils.molecule_utils import Molecule

TARGET_NAMES = listdir('models')
FING_COLUMNS = [f"Morgan_{i}" for i in range(1, 2049)]


st.set_page_config(
    page_title='Single pIC50 Predictor',
    page_icon='🧪'
)

st.title("Single pIC50 Predictor")

target_input = st.selectbox(label='Target human protein', options=TARGET_NAMES)

if target_input:
    desc_fing_options = [dfo.title() for dfo in listdir(f"models/{target_input}")]
    desc_fing_input = st.selectbox(label='Predictions based on descriptors or Morgan fingerprints?',
                                   options=desc_fing_options)
    smiles_input = st.text_input(label='SMILES', max_chars=5000)

    if st.button(label='Predict pIC50'):
        if not smiles_input:
            st.error('No SMILES was entered!', icon="🚨")
        else:
            molecule = Molecule(smiles_input)

            if not molecule.is_valid_smiles():
                st.error('Incorrect SMILES was entered!'
                         ' Correct SMILES according to the notation:'
                         ' https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system#Description',
                         icon="🚨")

            elif desc_fing_input == 'Descriptors':
                preprocessor_imputer_path = f"models/{target_input}/descriptors/preprocessor_imputer.joblib"
                selected_features_path = f"models/{target_input}/descriptors/selected_features.json"
                model_path = f"models/{target_input}/descriptors/model"

                preprocessor_imputer = joblib.load(preprocessor_imputer_path).set_output(transform='pandas')
                selected_features = load_selected_features(selected_features_path)
                model = load_model(model_path)

                descriptors_df = pd.DataFrame(molecule.generate_descriptors(), index=[0])
                descriptors_df = preprocess_descriptors(descriptors_df,
                                                        preprocessor_imputer,
                                                        selected_features)

                process_molecule(smiles_input, target_input, molecule, model, descriptors_df)

            elif desc_fing_input == 'Fingerprints':
                selected_features_path = f"models/{target_input}/fingerprints/selected_features.json"
                model_path = f"models/{target_input}/fingerprints/model"

                selected_features = load_selected_features(selected_features_path)
                model = load_model(model_path)

                fingerprints_df = pd.DataFrame(molecule.generate_fingerprints(), index=[0])
                fingerprints_df = preprocess_fingerprints(fingerprints_df, selected_features)

                process_molecule(smiles_input, target_input, molecule, model, fingerprints_df)
