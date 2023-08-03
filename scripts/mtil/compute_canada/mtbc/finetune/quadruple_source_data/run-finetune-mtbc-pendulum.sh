#!/bin/bash

module load python/3.9
module load mujoco
source ~/jaxl_env/bin/activate


python ../../../sweep_finetune_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/finetune_mtbc.json \
    --out_dir=${HOME}/scratch/data/finetune_mtbc_main-quadruple_source_data \
    --run_seed=0 \
    --num_runs=1 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/pendulum_cont \
    --num_heldouts=10 \
    --pretrain_dir=${HOME}/scratch/data/pretrain_mtbc_main-quadruple_source_data/pendulum-quadruple_source_data/continuous \
    --num_samples=1000 \
    --exp_name=pendulum-quadruple_source_data


python ../../../sweep_finetune_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/finetune_mtbc.json \
    --out_dir=${HOME}/scratch/data/finetune_mtbc_main-quadruple_source_data \
    --run_seed=0 \
    --num_runs=1 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/pendulum_disc \
    --num_heldouts=10 \
    --pretrain_dir=${HOME}/scratch/data/pretrain_mtbc_main-quadruple_source_data/pendulum-quadruple_source_data/discrete \
    --num_samples=1000 \
    --discrete_control \
    --exp_name=pendulum-quadruple_source_data

chmod +x run_all-*.sh
sbatch run_all-finetune-mtbc-single_sweep-pendulum-quadruple_source_data_continuous.sh
sbatch run_all-finetune-mtbc-single_sweep-pendulum-quadruple_source_data_discrete.sh