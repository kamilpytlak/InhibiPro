import streamlit as st

st.set_page_config(
    page_title='Homepage',
    page_icon='🏠'
)

DRUG_HUNTER_IMAGE = 'img/inhibipro_logo.jpg'

col1, col2 = st.columns(2)

with col1:
    st.image(DRUG_HUNTER_IMAGE, width=250)

with col2:
    st.title('InhibiPro - application for predicting drug bioactivity')

st.markdown(
    """
    InhibiPro is a powerful application designed for predicting pIC50 values for human protein inhibitors.
    With its advanced machine learning algorithms and comprehensive database of protein structures,
    this app provides accurate and reliable predictions for drug developers and researchers.
    
    **Key features:**
    
    *  🧪**Predict pIC50 Values**: Utilizing state-of-the-art predictive models, InhibiPro 
    calculates the pIC50 values for various human protein inhibitors. This information is crucial for assessing the 
    potency and efficacy of potential drugs. Users can choose from a range of 282 human proteins for which they want 
    to predict drug bioactivity. Proteins like Acetylcholinesterase and Monoamine oxidase can be selected based on the user's 
    specific needs.
    
    *  📙**Extensive Protein Database**: InhibiPro incorporates a vast collection of human protein 
    structures, including known inhibitors and their associated pIC50 values. This comprehensive database enhances 
    the accuracy and reliability of predictions.
    
    *  📦**Predictive Models**: The application provides efficient machine 
    learning models, including XGBoost, Random Forest, LightGBM, and neural networks, to ensure accurate 
    predictions of pharmacological activity.
    
    *  🙋**Descriptor and Fingerprint Options**: Users have the flexibility to 
    choose between molecular descriptors or Morgan fingerprints as the basis for their predictions. Both options 
    offer reliable methods for analyzing chemical compounds.
    
    *  ⚛️**2D Spatial Structure Visualization**: For every 
    SMILES input provided by the user, the application generates a two-dimensional spatial structure representation 
    of the compound. This visual aid helps users better understand the chemical structure they are working with.
    
    *  📏**Similar Compound Identification**: The application displays similar chemical compounds based on a minimum of 
    70% structural similarity to the user-inputted compound. This feature allows users to explore related compounds 
    that may exhibit similar bioactivity.
    
    *  💻**User-friendly Interface**: InhibiPro offers a user-friendly 
    interface, written in Streamlit, making it easy for researchers and drug developers to navigate and obtain 
    predictions. The intuitive design streamlines the prediction process and ensures efficient use of the 
    application.
    
    *  💾**Export and Save Results**: Users can export the predicted pIC50 values and associated data for 
    further analysis or integration into their research workflow. The application also enables saving and organizing 
    prediction results for future reference."""
)
