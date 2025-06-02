./pycbc_make_lisa_kde_inference \
--population-draw-file sobhb_gwtc3_bbh_mean_total_15yrs_seed_1_989590.hdf \
--injection-file-folder /work/shichao.wu/Area51/coherent_multiband_prod/population_run/multiverse_seed_1/injection_above_snr_threshold_seed_1_obs_1.0yrs_wait_5.0yrs/ \
--injection-snr-duration-file snr_seed_1_obs_1.0yrs_wait_5.0yrs.csv \
--lisa-obs-duration 1 \
--inference-config prior_lisa_kde.ini \
--config-files workflow_lisa_kde.ini \
--workflow-name lisa_kde_workflow_seed_1_obs_1yr_wait_5yrs_nessai \
--output-dir ./output_lisa_kde_seed_1_obs_1yr_wait_5yrs_nessai --submit-now
