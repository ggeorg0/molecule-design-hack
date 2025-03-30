"""Use RDKit's filter catalogs to filter for unwanted structures"""
from __future__ import annotations
__all__ = ["CornealPermeability"]

import logging

import joblib

from numpy.typing import NDArray

logger = logging.getLogger("reinvent")

from sklearn.preprocessing import MinMaxScaler

from sklearn.ensemble import ExtraTreesRegressor

from reinvent_plugins.normalize import normalize_smiles
from reinvent_plugins.components.add_tag import add_tag
from reinvent_plugins.components.component_results import ComponentResults

from config import MODELS_SAVE_PATH
from custom_scoring.helpers import extract_decriptors

MODEL_NAME = "ET_reg_sel_model.pkl"
SCALER_NAME = "minmax_scaler.pkl"

TRAINED_PARAMS = ['NHOHCount', 'MolLogP', 'MinAbsPartialCharge', 'NumHeterocycles', 'EState_VSA2', 'NOCount', 'fr_aniline', 'EState_VSA4', 'MaxAbsEStateIndex', 'BCUT2D_MRLOW', 'SlogP_VSA8', 'MaxEStateIndex', 'PEOE_VSA6', 'PEOE_VSA7', 'fr_Al_COO', 'SMR_VSA7', 'SlogP_VSA4', 'SMR_VSA2', 'MinEStateIndex', 'fr_bicyclic', 'NumHDonors', 'FpDensityMorgan1', 'TPSA', 'BCUT2D_LOGPLOW', 'NumHeteroatoms', 'PEOE_VSA9', 'SlogP_VSA7', 'qed', 'BCUT2D_MRHI', 'MaxPartialCharge', 'SMR_VSA4', 'SMR_VSA3', 'PEOE_VSA11', 'PEOE_VSA2', 'EState_VSA7', 'NumSaturatedHeterocycles', 'MinAbsEStateIndex', 'fr_COO2', 'fr_COO', 'SlogP_VSA6', 'VSA_EState2', 'VSA_EState3', 'fr_NH0', 'SlogP_VSA10', 'VSA_EState10', 'EState_VSA3', 'HallKierAlpha', 'VSA_EState5', 'NumAliphaticHeterocycles', 'PEOE_VSA14', 'NumHAcceptors', 'SlogP_VSA5', 'BalabanJ', 'fr_NH1', 'EState_VSA6', 'EState_VSA8', 'FpDensityMorgan2', 'NumBridgeheadAtoms', 'fr_Al_OH_noTert', 'AvgIpc', 'NumAliphaticCarbocycles', 'PEOE_VSA8', 'BCUT2D_MWHI', 'EState_VSA10', 'MinPartialCharge', 'fr_Al_OH', 'fr_ketone', 'fr_halogen', 'fr_sulfide', 'NumSaturatedCarbocycles', 'VSA_EState4', 'PEOE_VSA4', 'SlogP_VSA2', 'BCUT2D_MWLOW', 'SMR_VSA10', 'FpDensityMorgan3', 'fr_ether', 'NumRotatableBonds', 'PEOE_VSA12', 'VSA_EState8', 'BCUT2D_LOGPHI', 'SlogP_VSA11', 'NumAromaticCarbocycles', 'PEOE_VSA10', 'Phi', 'fr_Ar_N', 'fr_aryl_methyl', 'RingCount', 'Kappa2', 'fr_benzene', 'FractionCSP3', 'VSA_EState1', 'VSA_EState7', 'fr_pyridine', 'Chi1v', 'Kappa3', 'EState_VSA9', 'LabuteASA', 'BCUT2D_CHGHI', 'SMR_VSA1', 'Chi4v', 'VSA_EState9', 'PEOE_VSA3', 'fr_ketone_Topliss', 'SlogP_VSA12', 'fr_Ndealkylation1', 'Chi4n', 'Chi3v', 'fr_unbrch_alkane', 'fr_ester', 'EState_VSA1', 'VSA_EState6', 'MaxAbsPartialCharge', 'SlogP_VSA3', 'HeavyAtomCount', 'PEOE_VSA1', 'MolWt', 'SlogP_VSA1', 'PEOE_VSA13', 'ExactMolWt', 'Chi0n', 'fr_nitrile', 'fr_Ar_OH', 'BCUT2D_CHGLO', 'fr_NH2', 'SMR_VSA9', 'fr_allylic_oxid', 'SPS', 'fr_phenol_noOrthoHbond', 'fr_C_O', 'fr_thiazole', 'SMR_VSA6', 'NumAliphaticRings', 'Chi0v', 'EState_VSA5', 'Chi2v', 'NumAromaticHeterocycles', 'SMR_VSA5', 'BertzCT', 'fr_ArN', 'NumAromaticRings', 'fr_C_O_noCOO', 'Chi1', 'HeavyAtomMolWt', 'Kappa1', 'Chi0', 'fr_piperdine', 'Chi2n', 'fr_priamide', 'fr_sulfonamd', 'NumAmideBonds', 'NumValenceElectrons', 'MolMR', 'NumSaturatedRings', 'NumAtomStereoCenters', 'fr_phenol', 'Chi3n', 'fr_lactam', 'fr_lactone', 'NumUnspecifiedAtomStereoCenters', 'fr_Ar_NH', 'fr_amide', 'fr_furan', 'Chi1n']



@add_tag("__component")
class CornealPermeability:
    def __init__(self, params):
        print(params)
        model_path = MODELS_SAVE_PATH.joinpath(MODEL_NAME)
        print(model_path)
        scaler_path = MODELS_SAVE_PATH.joinpath(SCALER_NAME)
        extratreesregressor = joblib.load(model_path)
        minmaxscaler = joblib.load(scaler_path)

        self.model = extratreesregressor
        self.scaler = minmaxscaler
        self.smiles_type = "rdkit_smiles"

    @normalize_smiles
    def __call__(self, smiles: list[str]) -> NDArray:
        descriptors_df = extract_decriptors(smiles)
        descriptors_df = descriptors_df[TRAINED_PARAMS]
        descriptors_df = self.scaler.transform(descriptors_df)
        y_pred = self.model.predict(descriptors_df)
        return ComponentResults([y_pred])


