
<h1 align="center">
  <br>
  <a href="https://inhibipro.streamlit.app/"><img src="img/inhibipro_logo.jpg" alt="InhibiPro logo" width="250"></a>
  <br>
  InhibiPro
  <br>
</h1>

<h4 align="center">A web-based application designed for predicting the pharmacological activity of new drugs<br>built on top of <a href="https://streamlit.io/" target="_blank">Streamlit</a>.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#contact">Contact</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

![screenshot](img/inhibipro.gif)

<p align="center">
InhibiPro is a powerful web-based application for predicting pIC50 values for human protein inhibitors (potential new drugs). Based on the QSAR methodology and state-of-the-art machine learning algorithms, as well as a comprehensive database of protein structures, InhibiPro provides accurate and reliable predictions for drug developers and researchers.
</p>

## Key Features

*  🧪 **Predict pIC50 Values**: Using state-of-the-art prediction models, InhibiPro calculates the pIC50 values for various human protein inhibitors. This information is critical in assessing the potency and efficacy of potential drugs. Users can choose from a range of 336 human proteins for which they wish to predict drug bioactivity. Proteins such as acetylcholinesterase and HERG can be selected according to the user's specific needs.


*  📙 **Comprehensive Protein Database**: InhibiPro includes an extensive collection of human protein structures, including known inhibitors and their associated pIC50 values. This extensive database increases the accuracy and reliability of predictions.


*  📦 **Powerful Predictive Models**: The application provides powerful machine learning models, including Random Forest, k-Nearest Neighbours, LightGBM and neural networks, to ensure accurate prediction of pharmacological activity.


*  🙋 **Predictions Based on Descriptor or Fingerprint Data**: Users have the flexibility to choose between molecular descriptors or Morgan fingerprints as the basis for their predictions. Both options provide reliable methods for analysing chemical compounds.


*  ⚛️ **2D Spatial Structure Visualization**: For each SMILES input provided by the user, the application generates a two-dimensional spatial structure representation of the compound. This visual aid helps users better understand the chemical structure they are working with.


*  📏 **Identification of Similar Compounds**: The application displays similar chemical compounds based on a minimum of 70% structural similarity to the compound entered by the user. This feature allows users to explore related compounds that may have similar bioactivity.


*  💻 **User-friendly Interface**: InhibiPro offers a user-friendly interface, written in Streamlit, that makes it easy for researchers and drug developers to navigate and obtain predictions. The intuitive design streamlines the prediction process and ensures efficient use of the application.


*  💾 **Export and Save Results**: Users can export predicted pIC50 values and associated data for further analysis or integration into their research workflow. The application also allows users to save and organize prediction results for future reference.

## How To Use

There are two ways to use this tool:

1. Directly from the website: https://InhibiPro.streamlit.app/.
2. Clone the repository (using git or by downloading it directly from the website), install the dependencies from the configuration file `Pipfile` and launch the app locally using a browser.

```bash
# Clone this repository
$ git clone https://github.com/kamilpytlak/InhibiPro

# Go into the repository
$ cd InhibiPro

# Install pipenv (in case it's not installed) and, run pipenv shell and install dependencies
$ pip install pipenv
$ pipenv shell
$ pipenv install

# Ensure that the streamlit package was installed successfully.
$ streamlit hello

# Finally, run the app locally
$ streamlit run ./Homepage.py
```

## Contact

If you have any problems, ideas or general feedback, please don't hesitate to contact me at [kam.pytlak@gmail.com](mailto:kam.pytlak@gmail.com). I'd really appreciate it!

## Credits

This software uses the following open source packages:

- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [scikit-learn](https://scikit-learn.org/stable/#)
- [scikit-learn-intelex](https://intel.github.io/scikit-learn-intelex/)
- [lightgbm](https://lightgbm.readthedocs.io/en/latest/index.html)
- [xgboost](https://xgboost.readthedocs.io/en/latest/index.html)
- [tensor-flow](https://www.tensorflow.org/)
- [RDKit](https://www.rdkit.org/docs/index.html#)
- [chembl_webresource_client](https://github.com/chembl/chembl_webresource_client)

## License
MIT

---

> GitHub [@kamilpytlak](https://github.com/kamilpytlak) &nbsp;&middot;&nbsp;
> LinkedIn [kamil-pytlak](https://www.linkedin.com/in/kamil-pytlak/)

