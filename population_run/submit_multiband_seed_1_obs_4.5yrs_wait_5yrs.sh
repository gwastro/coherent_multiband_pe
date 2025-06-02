./pycbc_make_multiband_inference \
--population-draw-file sobhb_gwtc3_bbh_mean_total_15yrs_seed_1_989590.hdf \
--injection-file-folder /work/shichao.wu/Area51/coherent_multiband_prod/population_run/multiverse_seed_1/injection_above_snr_threshold_seed_1_obs_4.5yrs_wait_5.0yrs/ \
--injection-snr-duration-file snr_seed_1_obs_4.5yrs_wait_5.0yrs.csv \
--lisa-obs-duration 4.5 \
--inference-config prior_multiband.ini \
--config-files workflow_multiband.ini \
--workflow-name multiband_workflow_seed_1_obs_4.5yrs_wait_5yrs_nessai \
--output-dir ./output_multiband_seed_1_obs_4.5yrs_wait_5yrs_nessai --submit-now
