from pandas import DataFrame
from rdkit.Chem import Descriptors, MolFromSmiles
from rdkit.ML.Descriptors.MoleculeDescriptors import MolecularDescriptorCalculator

_DESCRIPTORS = [desc[0] for desc in Descriptors.descList]

def _get_descriptor_values(mol, descriptors):
    calc = MolecularDescriptorCalculator(descriptors)
    return calc.CalcDescriptors(mol)

def extract_decriptors(smiles_list: list[str]) -> DataFrame:
    mol_list = [MolFromSmiles(smiles) for smiles in smiles_list]
    descriptor_values = [_get_descriptor_values(mol, _DESCRIPTORS) for mol in mol_list if mol is not None]

    descriptor_df = DataFrame(descriptor_values, columns=_DESCRIPTORS)
    return descriptor_df