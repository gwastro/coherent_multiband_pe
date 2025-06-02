#!/bin/bash

for seed in {2..20}; do
    ./pycbc_make_multiband_inference \
    --population-draw-file "sobhb_gwtc3_bbh_mean_total_15yrs_seed_${seed}_989590.hdf" \
    --injection-file-folder "/work/shichao.wu/Area51/coherent_multiband_prod/population_run/multiverse_seed_${seed}/injection_above_snr_threshold_seed_${seed}_obs_7.5yrs_wait_5.0yrs/" \
    --injection-snr-duration-file "snr_seed_${seed}_obs_7.5yrs_wait_5.0yrs.csv" \
    --lisa-obs-duration 7.5 \
    --inference-config prior_multiband.ini \
    --config-files workflow_multiband.ini \
    --workflow-name "multiband_workflow_seed_${seed}_obs_7.5yrs_wait_5yrs_nessai" \
    --output-dir "./output_multiband_seed_${seed}_obs_7.5yrs_wait_5yrs_nessai" --submit-now
done
