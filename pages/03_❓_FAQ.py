import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title='FAQ',
    page_icon='❓'
)

VENN_DIAGRAM_IMG = 'img/descriptors_fingerprints_venn.jpg'

with open('img/tSNE.html', encoding='utf-8') as f:
    tsne_html = f.read()


st.title('FAQ')


with st.expander('What is the purpose of this application?'):
    st.markdown("""
    The purpose of DrugHunter is to provide a powerful platform for predicting pIC50 values of human protein inhibitors. 
    This application utilizes advanced machine learning algorithms and an extensive database of protein structures 
    to offer accurate and reliable predictions for drug developers and researchers. DrugHunter employs a state-of-the-art 
    Quantitative Structure-Activity Relationship (QSAR) methodology, which involves analyzing the relationship between 
    the structural features of chemical compounds and their biological activities. By calculating pIC50 values using QSAR 
    models, which assess the potency and efficacy of potential drugs, DrugHunter aids in identifying promising compounds 
    for further development in the field of drug discovery. This approach leverages the understanding of molecular structures 
    and their impact on bioactivity to provide valuable insights for drug development efforts.
    
    $IC_{50}$ indicates the concentration of a substance that inhibits the activity of the target enzyme by 50%. 
    However, in chemoinformatics calculations (and for convenience), a logarithmic scale is used, converting $IC_{50}$ 
    to $pIC_{50}$ according to the equation:
    
    $pIC_{50} = -log_{10}(IC_{50})$
    """)


with st.expander('What models have been trained?'):
    st.markdown("""
        The initial idea was to create effective QSAR models for 493 human proteins, but in the end only 242 (for 
        molecular descriptors) and 267 (for Morgan "fingerprints") fit the requirements of a good prediction quality 
        assessment.
        
        For molecular descriptors:
        - 119 XGBoost models (about 49.2%),
        - 90 LightGBM models (about 37.2%),
        - 31 random forest models (about 12.8%),
        - 2 neural networks (about 0.8%).
        
        For Morgan fingerprints:
        - 129 XGBoost models (approx. 48.3%),
        - 82 LightGBM models (about 30.7%),
        - 54 random forest models (about 20.2%),
        - 2 neural networks (about 0.7%).
        """
    )
    st.image(VENN_DIAGRAM_IMG, width=400)

with st.expander('Why was each human protein modeled separately?'):
    st.markdown(
        """The specificity of each protein has a significant impact on the chemical activity of the compounds used to 
        inhibit it. Proteins within the same family generally share similar molecular descriptor profiles of the 
        molecules used to inhibit them, as well as $pIC_{50}$ activity (see t-SNE chart below). For this reason, 
        it is important to model each human protein separately. It's worth also noting that while modeling each
        human protein separately in QSAR can provide valuable insights, it also requires significant computational
        resources and data. Depending on the research goals and available resources, researchers may choose to focus
        on specific protein targets or use more generalized models that capture broader trends across protein families.
        """
    )
    components.html(tsne_html, width=650, height=650)

with st.expander('On what basis was the quality of the models estimated?'):
    st.markdown("""
    The following metrics were used to assess the predictive quality of the QSAR models: $MAE$, $R^2$ and $RMSE$.
    
    Since nonlinear models were used for the prediction of $pIC_{50}$ in the present study, the estimated metrics for 
    both the sets after 5-fold cross-validation and the test set were used for the final selection of the best predictive 
    models for the human protein data, following the recommendations proposed by Veerasamy et al. ([link](https://www.researchgate.net/profile/Ravichandran-Veerasamy/publication/284566093_Validation_of_QSAR_Models_-_Strategies_and_Importance/links/5ca57788458515f78522300e/Validation-of-QSAR-Models-Strategies-and-Importance.pdf))
    -  $R^2$ > $0.5$ after cross-validation;
    -  $R^2$ > $0.6$ for the test set;
    -  the range of biological activity should include at least one logarithmic unit.
    
    If there were at least two models meeting the above criteria for a single target protein, the one with the lowest 
    $RMSE$ value for the test set was selected from among them.
    """)
