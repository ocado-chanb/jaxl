#!/bin/bash

module load python/3.9
module load mujoco
source ~/jaxl_env/bin/activate

python search_expert.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/search_expert \
    --run_seed=0 \
    --env_seed=42 \
    --env_name=ParameterizedPendulum-v0 \
    --exp_name=pendulum

python search_expert.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/search_expert \
    --run_seed=0 \
    --env_seed=42 \
    --discrete_control \
    --env_name=ParameterizedPendulum-v0 \
    --exp_name=pendulum

python search_expert.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/search_expert \
    --run_seed=0 \
    --env_seed=42 \
    --env_name=DMCCheetah-v0 \
    --exp_name=cheetah

python search_expert.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/search_expert \
    --run_seed=0 \
    --env_seed=42 \
    --discrete_control \
    --env_name=DMCCheetah-v0 \
    --exp_name=cheetah

python search_expert.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/search_expert \
    --run_seed=0 \
    --env_seed=42 \
    --env_name=DMCWalker-v0 \
    --exp_name=walker

python search_expert.py \
    --main_path=${JAXL_PATH}/jaxl/main.py \
    --config_template=${JAXL_PATH}/scripts/mtil/experiments/configs/main/ppo.json \
    --out_dir=${HOME}/scratch/data/search_expert \
    --run_seed=0 \
    --env_seed=42 \
    --discrete_control \
    --env_name=DMCWalker-v0 \
    --exp_name=walker