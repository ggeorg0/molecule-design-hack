from __future__ import annotations

__all__ = ["CornealPermeability"]

import logging

import joblib

from config import MODELS_SAVE_PATH
from custom_scoring.helpers import extract_decriptors
from reinvent_plugins.components.add_tag import add_tag
from reinvent_plugins.components.component_results import ComponentResults
from reinvent_plugins.normalize import normalize_smiles

logger = logging.getLogger("reinvent")

MODEL_NAME = "ET_reg_sel_model.pkl"
SCALER_NAME = "minmax_scaler.pkl"

TRAINED_PARAMS = ['NHOHCount', 'MolLogP', 'MinAbsPartialCharge', 'EState_VSA4', 'fr_aniline', 'SlogP_VSA8', 'TPSA', 'PEOE_VSA6', 'EState_VSA2', 'NOCount', 'FpDensityMorgan1', 'MaxPartialCharge', 'NumHDonors', 'PEOE_VSA7', 'NumHeteroatoms', 'MinEStateIndex', 'SMR_VSA2', 'SMR_VSA7', 'PEOE_VSA9', 'BCUT2D_MRLOW', 'PEOE_VSA2', 'NumAliphaticHeterocycles', 'fr_bicyclic', 'SMR_VSA4', 'fr_NH0', 'SlogP_VSA7', 'SlogP_VSA6', 'SlogP_VSA4', 'SlogP_VSA10', 'PEOE_VSA14', 'MaxAbsEStateIndex', 'qed', 'fr_Al_COO', 'NumHAcceptors', 'EState_VSA3', 'MaxEStateIndex', 'BCUT2D_LOGPLOW', 'BCUT2D_MRHI', 'MinAbsEStateIndex', 'MinPartialCharge', 'SMR_VSA3', 'fr_COO2', 'SMR_VSA10', 'fr_sulfide', 'VSA_EState10', 'NumSaturatedCarbocycles', 'NumSaturatedHeterocycles', 'EState_VSA7', 'HallKierAlpha', 'PEOE_VSA8', 'SlogP_VSA2', 'VSA_EState4', 'BalabanJ', 'VSA_EState3', 'FractionCSP3', 'SlogP_VSA5', 'fr_Al_OH_noTert', 'PEOE_VSA11', 'BCUT2D_CHGLO', 'EState_VSA6', 'PEOE_VSA4', 'VSA_EState2', 'VSA_EState6', 'VSA_EState5', 'MaxAbsPartialCharge', 'SlogP_VSA1', 'fr_COO', 'BCUT2D_MWLOW', 'FpDensityMorgan3', 'fr_C_O_noCOO', 'EState_VSA9', 'Kappa3', 'fr_benzene', 'fr_ether', 'VSA_EState8', 'EState_VSA8', 'fr_Al_OH', 'EState_VSA1', 'fr_pyridine', 'BCUT2D_MWHI', 'VSA_EState7', 'fr_ketone', 'SMR_VSA6', 'VSA_EState1', 'NumRotatableBonds', 'EState_VSA5', 'FpDensityMorgan2', 'SMR_VSA1', 'fr_NH2', 'NumAliphaticRings', 'fr_allylic_oxid', 'fr_Ar_OH', 'AvgIpc', 'fr_piperdine', 'BCUT2D_CHGHI', 'BertzCT', 'fr_Ar_N', 'NumAromaticRings', 'PEOE_VSA5', 'BCUT2D_LOGPHI', 'ExactMolWt', 'Chi4v', 'fr_amide', 'fr_halogen', 'Chi2v', 'fr_phenol_noOrthoHbond', 'PEOE_VSA10', 'SlogP_VSA3', 'NumAromaticHeterocycles', 'Chi1n', 'fr_aryl_methyl', 'PEOE_VSA12', 'PEOE_VSA1', 'MolWt', 'fr_methoxy', 'fr_thiazole', 'fr_ArN', 'RingCount', 'PEOE_VSA3', 'NumValenceElectrons', 'Chi1v', 'fr_ketone_Topliss', 'NumAliphaticCarbocycles', 'SlogP_VSA11', 'Chi0v', 'fr_C_O', 'Chi0n', 'HeavyAtomMolWt', 'fr_NH1', 'fr_Ndealkylation1', 'SPS', 'Chi1', 'fr_ester', 'EState_VSA10', 'NumAromaticCarbocycles', 'SMR_VSA5', 'fr_phenol', 'SMR_VSA9', 'fr_sulfonamd', 'Kappa2', 'Chi3v', 'Chi3n', 'HeavyAtomCount', 'fr_Imine', 'fr_Ndealkylation2', 'fr_para_hydroxylation', 'LabuteASA', 'VSA_EState9', 'fr_Nhpyrrole', 'Kappa1', 'SlogP_VSA12', 'fr_lactam', 'Chi4n', 'Chi0', 'fr_unbrch_alkane', 'fr_nitrile']


@add_tag("__component")
class CornealPermeability:
    def __init__(self, params):
        model_path = MODELS_SAVE_PATH.joinpath(MODEL_NAME)
        scaler_path = MODELS_SAVE_PATH.joinpath(SCALER_NAME)
        extratreesregressor = joblib.load(model_path)
        minmaxscaler = joblib.load(scaler_path)

        self.model = extratreesregressor
        self.scaler = minmaxscaler
        self.smiles_type = "rdkit_smiles"

    @normalize_smiles
    def __call__(self, smiles: list[str]) -> ComponentResults:
        descriptors_df = extract_decriptors(smiles)
        descriptors_df = descriptors_df[TRAINED_PARAMS].to_numpy()
        scaled_features = self.scaler.transform(descriptors_df)
        y_pred = self.model.predict(scaled_features)
        return ComponentResults([y_pred])


