import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title='FAQ',
    page_icon='❓'
)


with open('img/tSNE.html', encoding='utf-8') as f:
    tsne_html = f.read()


st.title('FAQ')


with st.expander('What models have been trained?'):
    st.write('Text')

with st.expander('Why was each human protein modeled separately?'):
    st.markdown(
        """The specificity of each protein has a significant impact on the chemical activity of the compounds used to 
        inhibit it. Proteins within the same family generally share similar molecular descriptor profiles of the 
        molecules used to inhibit them, as well as $pIC_{50}$ activity (see t-SNE chart below). For this reason, 
        it is important to model each human protein separately."""
    )
    components.html(tsne_html, width=650, height=650)

with st.expander('How much data was used for training?'):
    st.markdown(
        """The initial idea was to create effective QSAR models for 487 human proteins, but in the end only 336 (for 
        molecular descriptors) and 307 (for Morgan "fingerprints") fit the requirements of a good prediction quality 
        assessment. Only those proteins for which the number tested was not less than 200 were included in the 
        modeling."""
    )

with st.expander('On what basis was the quality of the models estimated?'):
    st.write('Text')
