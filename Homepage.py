import os

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title='Homepage',
    page_icon='🏠'
)

# Constants
DRUG_HUNTER_IMAGE = 'img/inhibipro_logo.jpg'


# Function to safely load the image
def load_image(image_path: str, width: int = 250):
    if os.path.exists(image_path):
        st.image(image_path, width=width)
    else:
        st.warning(f"Image not found: {image_path}")


# Layout: Two columns
col1, col2 = st.columns(2)

with col1:
    load_image(DRUG_HUNTER_IMAGE)

with col2:
    st.title('InhibiPro - Application for Predicting Drug Bioactivity')

# Description of the application
st.markdown(
    """
    InhibiPro is a powerful application designed for predicting pIC50 values for human protein inhibitors.
    With its advanced machine learning algorithms and comprehensive database of protein structures,
    this app provides accurate and reliable predictions for drug developers and researchers.

    **Key Features:**

    *  🧪 **Predict pIC50 Values**: Utilizing state-of-the-art predictive models, InhibiPro 
    calculates the pIC50 values for various human protein inhibitors. This information is crucial for assessing the 
    potency and efficacy of potential drugs. Users can choose from a range of 282 human proteins, including proteins 
    like Acetylcholinesterase and Monoamine oxidase.

    *  📙 **Extensive Protein Database**: InhibiPro incorporates a vast collection of human protein 
    structures, including known inhibitors and their associated pIC50 values. This comprehensive database enhances 
    the accuracy and reliability of predictions.

    *  📦 **Predictive Models**: The application provides efficient machine learning models, 
    including XGBoost, Random Forest, LightGBM, and neural networks, to ensure accurate predictions of pharmacological activity.

    *  🙋 **Descriptor and Fingerprint Options**: Users have the flexibility to 
    choose between molecular descriptors or Morgan fingerprints as the basis for their predictions. Both options 
    offer reliable methods for analyzing chemical compounds.

    *  ⚛️ **2D Spatial Structure Visualization**: For every 
    SMILES input provided by the user, the application generates a two-dimensional spatial structure representation 
    of the compound.

    *  📏 **Similar Compound Identification**: The application displays similar chemical compounds based on a minimum of 
    70% structural similarity to the user-inputted compound.

    *  💻 **User-friendly Interface**: InhibiPro offers a user-friendly 
    interface, written in Streamlit, making it easy for researchers and drug developers to navigate and obtain 
    predictions.

    *  💾 **Export and Save Results**: Users can export the predicted pIC50 values and associated data for 
    further analysis or integration into their research workflow.
    """
)
