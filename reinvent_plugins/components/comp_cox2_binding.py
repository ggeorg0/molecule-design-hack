from __future__ import annotations

__all__ = ["COX2Binding"]

import logging

import numpy as np
from meeko import MoleculePreparation
from rdkit.Chem import AddHs, MolFromSmiles, rdCoordGen
from vina import Vina

from config import BINDING_CENTER, BOX_SIZE, RECEPTOR_PATH
from reinvent_plugins.components.add_tag import add_tag
from reinvent_plugins.components.component_results import ComponentResults
from reinvent_plugins.normalize import normalize_smiles

logger = logging.getLogger("reinvent")

@add_tag("__component")
class COX2Binding:
    def __init__(self, params):
        self.receptor_file = RECEPTOR_PATH.__str__()
        self._meeko_prep = MoleculePreparation()

        self.smiles_type = "rdkit_smiles"

    def _compute_energy(self, smiles: str) -> float:
        _v = Vina(sf_name='vina')
        _v.set_receptor(self.receptor_file)
        lig = MolFromSmiles(smiles)
        protonated_lig = AddHs(lig)
        rdCoordGen.AddCoords(protonated_lig)
        self._meeko_prep.prepare(protonated_lig)
        lig_pdbqt = self._meeko_prep.write_pdbqt_string()
        _v.set_ligand_from_string(lig_pdbqt)
        _v.compute_vina_maps(
            center=BINDING_CENTER,
            box_size=BOX_SIZE
        )
        _v.dock(exhaustiveness=4, n_poses=4)
        # we add minus to optimize this param
        return - _v.score()[0]

    @normalize_smiles
    def __call__(self, smiles: list[str]) -> ComponentResults:
        energies = np.array([self._compute_energy(s) for s in smiles])
        return ComponentResults([energies])
