# -*- coding: utf-8 -*-

import os
import glob
import configparser
import csv
import pandas as pd
from tqdm import tqdm

# GW190521 reference parameters and confidence intervals (source frame)
gw_params = {
    "mass1": 85.0,
    "mass2": 66.0,
    "spin_eff": 0.08,
    "dl": 5.3  # Luminosity distance in Gpc
}
confidence_intervals = {
    "mass1": (71, 106),  # 71 ≤ M1 ≤ 106
    "mass2": (48, 83),  # 48 ≤ M2 ≤ 83
    "spin_eff": (-0.28, 0.35),  # χ_eff ∈ [-0.28, 0.35]
    "dl": (2.7, 7.7)  # 2.7 ≤ dl ≤ 7.7 Gpc
}
redshift = 0.82  # GW190521 redshift

def parse_folder_name(folder_path):
    """Parse folder name to extract seed and obs values"""
    folder_name = os.path.basename(folder_path)
    parts = folder_name.split("_")
    seed = parts[3]
    obs_str = parts[5].replace("yrs", "")
    obs = float(obs_str)
    return seed, obs

def parse_ini_file(file_path):
    """Parse INI file to extract parameters"""
    config = configparser.ConfigParser()
    config.read(file_path)
    
    if "specific" not in config:
        raise ValueError(f"Missing [specific] section in {file_path}")
    
    data = {}
    # Required parameters
    data["mass1"] = float(config["specific"]["mass1"])
    data["mass2"] = float(config["specific"]["mass2"])
    data["spin1z"] = float(config["specific"]["spin1z"])
    data["spin2z"] = float(config["specific"]["spin2z"])
    data["dl_min"] = float(config["specific"]["dl_min"])
    data["dl_max"] = float(config["specific"]["dl_max"])
    
    return data

def is_within_ci(source_mass1, source_mass2, spin_eff, dl):
    """Check if parameters are within GW190521's 90% confidence intervals"""
    if not (confidence_intervals["mass1"][0] <= source_mass1 <= confidence_intervals["mass1"][1]):
        return False
    if not (confidence_intervals["mass2"][0] <= source_mass2 <= confidence_intervals["mass2"][1]):
        return False
    if not (confidence_intervals["spin_eff"][0] <= spin_eff <= confidence_intervals["spin_eff"][1]):
        return False
    if not (confidence_intervals["dl"][0] <= dl <= confidence_intervals["dl"][1]):
        return False
    return True

def calculate_similarity(data):
    """Calculate similarity metrics with unit conversion"""
    # Source frame masses
    source_mass1 = data["mass1"] / (1 + redshift)
    source_mass2 = data["mass2"] / (1 + redshift)
    total_mass = source_mass1 + source_mass2
    
    # Effective spin calculation
    spin_eff = (
        data["spin1z"] * source_mass1 + 
        data["spin2z"] * source_mass2
    ) / total_mass
    
    # Convert dl from Mpc to Gpc
    dl = (data["dl_min"] + data["dl_max"]) / 2 / 1000  # 1 Gpc = 1000 Mpc
    
    # Compute parameter differences
    diff_mass1 = abs(source_mass1 - gw_params["mass1"])
    diff_mass2 = abs(source_mass2 - gw_params["mass2"])
    diff_spin_eff = abs(spin_eff - gw_params["spin_eff"])
    diff_dl = abs(dl - gw_params["dl"])
    
    # Weighted Euclidean distance (mass:3x, spin_eff:200x, dl:20x)
    weighted_diff = (
        3*(diff_mass1**2 + diff_mass2**2) + 
        200*(diff_spin_eff**2) + 
        20*(diff_dl**2)
    ) ** 0.5
    
    return weighted_diff, dl, source_mass1, source_mass2, spin_eff

def main():
    base_dir = "/work/shichao.wu/Area51/coherent_multiband_prod/population_run/"
    folder_pattern = "output_multiband_seed_*_obs_*yrs_wait_5yrs_nessai"
    all_folders = glob.glob(os.path.join(base_dir, folder_pattern))
    
    results = []
    
    # Main progress bar for folders
    for folder in tqdm(all_folders, desc="Processing folders", unit="folder"):
        try:
            seed, obs = parse_folder_name(folder)
            
            # Filter for obs=7.5
            if obs != 7.5:
                continue
                
            ini_pattern = os.path.join(folder, "specific_prior_inj_*_multiband.ini")
            ini_files = glob.glob(ini_pattern)
            
            # Read SNR file using index column as injection ID
            obs_str = f"{obs:.1f}"
            snr_filename = f"snr_seed_{seed}_obs_{obs_str}yrs_wait_5.0yrs.csv"
            snr_path = os.path.join(base_dir, snr_filename)
            
            try:
                # Read CSV and reset index to include it as a column
                snr_df = pd.read_csv(snr_path).reset_index()
                # Now, 'index' is the injection ID column
            except FileNotFoundError:
                print(f"SNR file not found: {snr_path}")
                snr_df = None
            
            # Sub-progress bar for INI files
            for ini_file in tqdm(ini_files, desc=f"Processing {seed}/{obs}", leave=False, unit="file"):
                # Extract injection number from filename
                filename = os.path.basename(ini_file)
                filename_parts = filename.split("_")
                inj = filename_parts[3].split(".")[0]  # inj is the number after "inj_"
                
                # Read parameters
                try:
                    data = parse_ini_file(ini_file)
                    total_diff, dl, source_mass1, source_mass2, spin_eff = calculate_similarity(data)
                    
                    # Check confidence intervals
                    if not is_within_ci(source_mass1, source_mass2, spin_eff, dl):
                        continue
                    
                    # Fetch SNR using the index column (injection ID)
                    if snr_df is not None:
                        try:
                            snr_lisa = snr_df[snr_df['index'] == int(inj)]['snr_lisa'].values[0]
                        except KeyError:
                            print(f"SNR file lacks 'index' column: {snr_path}")
                            snr_lisa = None
                        except IndexError:
                            print(f"Missing SNR for inj={inj} in {snr_path}")
                            snr_lisa = None
                    else:
                        snr_lisa = None
                    
                    result = {
                        "seed": seed,
                        "obs": obs,
                        "inj": inj,
                        "mass1": data["mass1"],
                        "mass2": data["mass2"],
                        "source_mass1": source_mass1,
                        "source_mass2": source_mass2,
                        "spin1z": data["spin1z"],
                        "spin2z": data["spin2z"],
                        "spin_eff": spin_eff,
                        "dl": dl,
                        "similarity": total_diff,
                        "snr_lisa": snr_lisa
                    }
                    results.append(result)
                except KeyError as e:
                    print(f"Missing parameter {e} in {ini_file}")
                except ValueError as e:
                    print(f"Error parsing {ini_file}: {str(e)}")
        except Exception as e:
            print(f"Error processing folder {folder}: {str(e)}")
    
    # Normalize similarity score (0-1 range)
    if not results:
        print("No valid results found. Exiting.")
        return
    
    min_sim = min(r["similarity"] for r in results if r["similarity"] is not None)
    max_sim = max(r["similarity"] for r in results if r["similarity"] is not None)
    
    for r in results:
        if max_sim == min_sim:
            r["normalized_similarity"] = 1.0
        else:
            r["normalized_similarity"] = (max_sim - r["similarity"]) / (max_sim - min_sim)
    
    # Sort by normalized_similarity descending (highest first)
    top100 = sorted(results, key=lambda x: -x["normalized_similarity"])[:100]
    
    # Save to CSV in specified directory
    output_dir = "/work/shichao.wu/Area51/coherent_multiband_prod/population_run/"
    csv_file = os.path.join(output_dir, "closest_simulations.csv")
    with open(csv_file, "w", newline="") as f:
        fieldnames = [
            "seed", "obs", "inj",
            "mass1", "mass2",
            "source_mass1", "source_mass2",
            "spin1z", "spin2z",
            "spin_eff",
            "dl", "similarity", "normalized_similarity",
            "snr_lisa"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top100)
    
    print(f"\nTop 100 matches saved to {csv_file}")
    print(f"Normalization range: Min={min_sim:.2f}, Max={max_sim:.2f}")

if __name__ == "__main__":
    print("Starting parameter analysis...")
    print("Install 'tqdm' and 'pandas' if not present: pip install tqdm pandas")
    main()