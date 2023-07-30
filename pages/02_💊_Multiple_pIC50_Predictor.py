from os import listdir

import joblib
import pandas as pd
import streamlit as st

from utils.model_utils import load_selected_features, load_model, preprocess_descriptors, preprocess_fingerprints, \
    convert_df
from utils.molecule_utils import Molecule

TARGET_NAMES = sorted(listdir('models'))
FING_COLUMNS = [f"Morgan_{i}" for i in range(1, 2049)]


st.set_page_config(
    page_title='Multiple pIC50 Predictor',
    page_icon='💊'
)

st.title("Multiple pIC50 Predictor")

target_input = st.selectbox(label='Target Input', options=TARGET_NAMES)

if target_input:
    desc_fing_options = [dfo.title() for dfo in listdir(f"models/{target_input}")]
    desc_fing_input = st.selectbox(label='Descriptor/Fingerprint', options=desc_fing_options)
    file_upload = st.file_uploader(label='Choose a file', type=['csv'])

    if st.button(label='Predict pIC50'):
        if not file_upload:
            st.error('No file selected!', icon="🚨")
        else:
            smiles_df = pd.read_csv(file_upload)

            if 'SMILES' not in smiles_df.columns:
                st.error('There is no "SMILES" column in the loaded data!'
                         ' Correct the column name to "SMILES".', icon="🚨")
            else:
                smiles = smiles_df['SMILES']
                molecules = smiles.apply(lambda row_smiles: Molecule(row_smiles))
                valid_molecules = molecules.apply(lambda mole: mole.is_valid_smiles())
                if not valid_molecules.all():
                    st.error('At least one SMILES is incorrect (inconsistent with notation)!'
                             ' Correct SMILES according to the notation:'
                             ' https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system#Description',
                             icon="🚨")
                else:
                    if desc_fing_input == 'Descriptors':
                        preprocessor_imputer_path = f"models/{target_input}/descriptors/preprocessor_imputer.joblib"
                        selected_features_path = f"models/{target_input}/descriptors/selected_features.json"
                        model_path = f"models/{target_input}/descriptors/model"

                        preprocessor_imputer = joblib.load(preprocessor_imputer_path).set_output(transform='pandas')
                        selected_features = load_selected_features(selected_features_path)
                        model = load_model(model_path)

                        descriptors_df = pd.DataFrame.from_records(
                            molecules.apply(lambda molecule: molecule.generate_descriptors())
                        )
                        descriptors_df = preprocess_descriptors(descriptors_df,
                                                                preprocessor_imputer,
                                                                selected_features)

                        predicted_pic50 = model.predict(descriptors_df).round(2)
                        smiles_df['Predicted pIC50'] = predicted_pic50

                        st.success('pIC50 prediction from a file successfully completed!', icon="✅")

                        csv = convert_df(smiles_df)
                        st.download_button(
                            label='Download prediction as CSV',
                            data=csv,
                            file_name='pic50_prediction.csv',
                            mime='text/csv'
                        )

                    elif desc_fing_input == 'Fingerprints':
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

                        st.success('SMILES prediction from a file successfully completed!', icon="✅")

                        csv = convert_df(smiles_df)
                        st.download_button(
                            label='Download data as CSV',
                            data=csv,
                            file_name='pic50_prediction.csv',
                            mime='text/csv'
                        )
