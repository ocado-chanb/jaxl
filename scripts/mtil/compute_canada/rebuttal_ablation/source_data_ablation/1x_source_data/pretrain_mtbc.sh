#!/bin/bash

module load python/3.9
module load mujoco
source ~/jaxl_env/bin/activate


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/cartpole_cont \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=500 \
    --samples_per_task \
    --exp_name=cartpole-1x_source_data \
    --num_epochs=5000 \
    --run_time=01:30:00


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/frozenlake_disc \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=500 \
    --samples_per_task \
    --discrete_control \
    --exp_name=frozenlake-1x_source_data \
    --num_epochs=5000 \
    --run_time=01:30:00


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/cheetah_cont \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=1000 \
    --exp_name=cheetah-1x_source_data \
    --samples_per_task \
    --run_time=01:30:00 \
    --num_epochs=5000


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/cheetah_disc \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=1000 \
    --discrete_control \
    --exp_name=cheetah-1x_source_data \
    --samples_per_task \
    --run_time=01:30:00 \
    --num_epochs=5000


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/pendulum_cont \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=1000 \
    --samples_per_task \
    --exp_name=pendulum-1x_source_data \
    --num_epochs=5000 \
    --run_time=02:00:00


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/pendulum_disc \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=1000 \
    --samples_per_task \
    --discrete_control \
    --exp_name=pendulum-1x_source_data \
    --num_epochs=5000 \
    --run_time=01:30:00


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/walker_cont \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=2000 \
    --exp_name=walker-1x_source_data \
    --samples_per_task \
    --run_time=01:30:00 \
    --num_epochs=5000


python ../../../sweep_pretrain_mtbc.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/pretrain_mtbc.json \
    --out_dir=${HOME}/scratch/data/pretrain_mtbc_main-1x_source_data \
    --run_seed=0 \
    --num_runs=5 \
    --hyperparam_set=single_sweep \
    --data_dir=${HOME}/scratch/data/expert_data/walker_disc \
    --num_heldouts=10 \
    --num_tasks_variants=1,2,4,8,16 \
    --num_samples=500 \
    --discrete_control \
    --exp_name=walker-1x_source_data \
    --samples_per_task \
    --run_time=01:30:00 \
    --num_epochs=5000

chmod +x run_all-*.sh
sbatch run_all-pretrain-mtbc-single_sweep-cartpole-1x_source_data_continuous.sh
sbatch run_all-pretrain-mtbc-single_sweep-frozenlake-1x_source_data_discrete.sh
sbatch run_all-pretrain-mtbc-single_sweep-cheetah-1x_source_data_continuous.sh
sbatch run_all-pretrain-mtbc-single_sweep-cheetah-1x_source_data_discrete.sh
sbatch run_all-pretrain-mtbc-single_sweep-pendulum-1x_source_data_continuous.sh
sbatch run_all-pretrain-mtbc-single_sweep-pendulum-1x_source_data_discrete.sh
sbatch run_all-pretrain-mtbc-single_sweep-walker-1x_source_data_continuous.sh
sbatch run_all-pretrain-mtbc-single_sweep-walker-1x_source_data_discrete.sh