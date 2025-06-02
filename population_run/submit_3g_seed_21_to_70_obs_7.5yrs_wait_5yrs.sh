#!/bin/bash

for seed in {21..70}; do
    output_dir="./output_3g_seed_${seed}_obs_7.5yrs_wait_5yrs_nessai"
    
    # Check if directory exists
    if [ -d "$output_dir" ]; then
        # Check if directory is empty
        if [ -z "$(ls -A "$output_dir")" ]; then
            # Directory exists and is empty: delete and proceed
            echo "Deleting empty directory: $output_dir"
            rm -rf "$output_dir"
            # Run the inference command and wait 15s
            ./pycbc_make_3g_inference \
            --population-draw-file "sobhb_gwtc3_bbh_mean_total_15yrs_seed_${seed}_989590.hdf" \
            --injection-file-folder "/work/shichao.wu/Area51/coherent_multiband_prod/population_run/multiverse_seed_${seed}/injection_above_snr_threshold_seed_${seed}_obs_7.5yrs_wait_5.0yrs/" \
            --injection-snr-duration-file "snr_seed_${seed}_obs_7.5yrs_wait_5.0yrs.csv" \
            --inference-config prior_3g.ini \
            --config-files workflow_3g.ini \
            --workflow-name "3g_workflow_seed_${seed}_obs_7.5yrs_wait_5yrs_nessai" \
            --output-dir "$output_dir" --submit-now; sleep 15
        else
            # Directory exists and is not empty: skip this seed
            echo "Skipping seed ${seed}: directory $output_dir is not empty"
            continue
        fi
    else
        # Directory does not exist: proceed directly
        echo "Directory $output_dir does not exist, proceeding..."
        ./pycbc_make_3g_inference \
        --population-draw-file "sobhb_gwtc3_bbh_mean_total_15yrs_seed_${seed}_989590.hdf" \
        --injection-file-folder "/work/shichao.wu/Area51/coherent_multiband_prod/population_run/multiverse_seed_${seed}/injection_above_snr_threshold_seed_${seed}_obs_7.5yrs_wait_5.0yrs/" \
        --injection-snr-duration-file "snr_seed_${seed}_obs_7.5yrs_wait_5.0yrs.csv" \
        --inference-config prior_3g.ini \
        --config-files workflow_3g.ini \
        --workflow-name "3g_workflow_seed_${seed}_obs_7.5yrs_wait_5yrs_nessai" \
        --output-dir "$output_dir" --submit-now; sleep 15
    fi
done