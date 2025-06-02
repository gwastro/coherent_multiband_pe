#!/bin/bash

gen_multiverse() {
    local seed=$1
    echo "Running gen_multiverse with seed $seed"

#    if ! pycbc_create_injections --verbose \
#        --config-files ./gwtc3_bbh_mean_total_15yrs.ini \
#        --ninjections 989590 \
#        --seed "$seed" \
#        --output-file "sobhb_gwtc3_bbh_mean_total_15yrs_seed_${seed}_989590.hdf" \
#        --variable-params-section variable_params \
#        --static-params-section static_params \
#        --dist-section prior \
#        --force; then
#        echo "Error creating injections for seed $seed" >&2
#        return 1
#    fi

    if ! ./check_optimal_snr_duration \
        --seed "$seed" \
        --dir-path /work/shichao.wu/Area51/coherent_multiband_prod \
        --injection-file-name "sobhb_gwtc3_bbh_mean_total_15yrs_seed_${seed}_989590" \
        --t-lisa-obs-cases "1 2 3 3.75 4.5 7.5" \
        --t-3g-wait-cases "5 5 5 5 5 5"; then
        echo "Error checking optimal SNR duration for seed $seed" >&2
        return 1
    fi

    echo "Completed gen_multiverse with seed $seed"
}

export -f gen_multiverse

seq 1 20 | xargs -P 20 -I {} bash -c 'gen_multiverse "$@"' _ {}
