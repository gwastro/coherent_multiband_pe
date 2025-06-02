./pycbc_make_3g_inference \
--population-draw-file sobhb_gwtc3_bbh_mean_total_15yrs_seed_1_989590.hdf \
--injection-file-folder /work/shichao.wu/Area51/coherent_multiband_prod/population_run/multiverse_seed_1/injection_above_snr_threshold_seed_1_obs_1.0yrs_wait_5.0yrs/ \
--injection-snr-duration-file snr_seed_1_obs_1.0yrs_wait_5.0yrs.csv \
--inference-config prior_3g.ini \
--config-files workflow_3g.ini \
--workflow-name 3g_workflow_seed_1_obs_1yr_wait_5yrs_nessai \
--output-dir ./output_3g_seed_1_obs_1yr_wait_5yrs_nessai --submit-now
