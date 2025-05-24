import os
import sys
from pyscf import gto, scf

# Example usage with python:
# python energy_calculations.py original_molecule_dir modified_molecule_dir

# Description:
# This script takes in a directory as the argument and will iterate through
# each csv file in the directory to calculate and prepend the HOMO-LUMO energy gap for those
# atoms and coordinates.

# This script is intended to prepare files for input to the qm9_create_tfdataset.ipynb notebook.

# If running the xyz_model.py program, you do not need to use this script.

# If 4 args are not provided, print usage and exit.
if len(sys.argv) != 2:
    print("Usage: python energy_calculations.py <original_dir>")
    print("Note: Input directory should only contain the csv files to be modified")
    sys.exit()
else:
    try:
        dir = sys.argv[1]
    except Exception as e:
        print("Usage: python energy_calculations.py <original_dir>")
        print("Note: Input directory should only contain the csv files to be modified")
        sys.exit()

# Function: homo_lumo_energy
def homo_lumo_energy(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        atom_str = '\n'.join(line.strip() for line in lines if line.strip()) # extracting each atom of the molecule in the file

    # First, count the total number of electrons in the molecule to use to determine its spin
    mol = gto.Mole() # creates an empty molecule object
    mol.atom = atom_str # assigns the atomic structure of molecule based on atoms (atom_str) extracted above
    mol.unit = 'Angstrom'
    mol.basis = 'sto-3g' # alternatively, choose the basis set of your own interest to represent your molecule orbitals
    mol.build() # builds the molecule
    nelec = mol.nelectron # counts the total number of electrons in the molecule

    # Fix spin: set spin = 0 for even no. electrions (nelec); or 1 for odd (i.e., doublet)
    spin = 0 if nelec % 2 == 0 else 1

    # Now re-build the molecule using the spin calculated above
    mol = gto.M(atom=atom_str, basis='sto-3g', unit='Angstrom', spin=spin)
    mf = scf.RHF(mol) # initialises a Restricted Hartree-Fock (RHF) calculation for the molecule
    mf.kernel() # executes RHF calculation

    # Calculate the respective HOMO and LUMO energies from RHF calculations above
    homo = mf.mo_energy[mf.mo_occ > 0][-1]
    lumo = mf.mo_energy[mf.mo_occ == 0][0]

    return lumo - homo

# Loop through each file in the input directory and append the energy gap
for filename in sorted(os.listdir(dir)):
    if not filename.endswith(".csv"):
        continue

    # Generate the full file path
    file_path = os.path.join(dir, filename)

    try:
        # Calculate the energy gap
        gap = homo_lumo_energy(file_path)

        # Open target file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Prepend energy gap as first line
        with open(file_path, 'w') as f:
            f.write(f"energy_gap,{gap:.6f}\n")
            f.writelines(lines)

    except Exception as e:
        print(f"Failed to process {filename}: {e}")
