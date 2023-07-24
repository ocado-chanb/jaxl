#!/bin/bash

module load python/3.9
module load mujoco
source ~/jaxl_env/bin/activate

python sweep_rl.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/hyperparam_sweep \
    --run_seed=0 \
    --env_name=ParameterizedPendulum-v0 \
    --exp_name=pendulum_cont \
    --num_envs=6 \
    --num_runs=3 \
    --hyperparam_set=hyperparam_sweep

python sweep_rl.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/hyperparam_sweep \
    --run_seed=0 \
    --env_name=ParameterizedPendulum-v0 \
    --exp_name=pendulum_disc \
    --discrete_control \
    --num_envs=6 \
    --num_runs=3 \
    --hyperparam_set=hyperparam_sweep

python sweep_rl.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/hyperparam_sweep \
    --run_seed=0 \
    --env_name=DMCCheetah-v0 \
    --exp_name=cheetah_cont \
    --num_envs=6 \
    --num_runs=3 \
    --hyperparam_set=hyperparam_sweep

python sweep_rl.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/hyperparam_sweep \
    --run_seed=0 \
    --env_name=DMCCheetah-v0 \
    --exp_name=cheetah_disc \
    --discrete_control \
    --num_envs=6 \
    --num_runs=3 \
    --hyperparam_set=hyperparam_sweep

python sweep_rl.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/hyperparam_sweep \
    --run_seed=0 \
    --env_name=DMCWalker-v0 \
    --exp_name=walker_cont \
    --num_envs=6 \
    --num_runs=3 \
    --hyperparam_set=hyperparam_sweep

python sweep_rl.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/hyperparam_sweep \
    --run_seed=0 \
    --env_name=DMCWalker-v0 \
    --exp_name=walker_disc \
    --discrete_control \
    --num_envs=6 \
    --num_runs=3 \
    --hyperparam_set=hyperparam_sweep

chmod +x run_all-*.sh
sbatch run_all-hyperparam_sweep-cheetah_discrete.sh
sbatch run_all-hyperparam_sweep-cheetah_continuous.sh
sbatch run_all-hyperparam_sweep-walker_discrete.sh
sbatch run_all-hyperparam_sweep-walker_continuous.sh
sbatch run_all-hyperparam_sweep-pendulum_discrete.sh
sbatch run_all-hyperparam_sweep-pendulum_continuous.sh