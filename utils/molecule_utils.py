from typing import List, Dict

from chembl_webresource_client.new_client import new_client
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, SaltRemover

FING_COLUMNS = [f"Morgan_{i}" for i in range(1, 2049)]


class Molecule:
    def __init__(self, smiles: str):
        self.smiles = smiles
        self.mol = Chem.MolFromSmiles(smiles)

    def is_valid_smiles(self):
        return self.mol is not None

    def remove_salt(self):
        remover = SaltRemover.SaltRemover()
        mol = remover.StripMol(self.mol, dontRemoveEverything=True)
        return mol

    def find_similar_molecules(self) -> List[Dict]:
        similarity = new_client.similarity
        similar_molecules = (similarity
                             .filter(smiles=self.smiles, similarity=70)
                             .only(['molecule_chembl_id', 'pref_name',
                                    'molecule_structures', 'similarity'])
                             )

        similar_molecules_final = []
        for similar_molecule in similar_molecules:
            try:
                canonical_smiles = similar_molecule['molecule_structures']['canonical_smiles']
            except TypeError:
                canonical_smiles = None

            similar_molecule.pop('molecule_structures', None)
            similar_molecule['canonical_smiles'] = canonical_smiles
            similar_molecules_final.append(similar_molecule)

        return similar_molecules_final

    def calculate_molecular_weight(self) -> float:
        return Descriptors.MolWt(self.mol)

    def generate_descriptors(self) -> dict:
        mol = self.remove_salt()
        descriptors = Descriptors.CalcMolDescriptors(mol)
        descriptors.pop('Ipc', None)
        return descriptors

    def generate_fingerprints(self) -> dict:
        mol = self.remove_salt()
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
        fp = fp.ToList()
        final_df = dict(zip(FING_COLUMNS, fp))
        return final_df
