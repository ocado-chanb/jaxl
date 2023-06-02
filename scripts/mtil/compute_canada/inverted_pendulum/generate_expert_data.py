""" Script for generating experiment for multitask imitation learning

Example command:
python generate_expert_data.py \
    --runs_dir=/home/chanb/scratch/jaxl/data/inverted_pendulum/expert_models/gravity/runs \
    --out_dir=/home/chanb/scratch/jaxl/data/inverted_pendulum/expert_data \
    --exp_name=gravity \
    --run_seed=0 \
    --env_seed=42 \
    --num_episodes=10 \
    --buffer_size=10000


This will generate a dat file that consists of various runs.
"""

from absl import app, flags
from absl.flags import FlagValues

import itertools
import jax
import json
import os


FLAGS = flags.FLAGS
flags.DEFINE_string(
    "exp_name",
    default=None,
    help="Experiment name",
    required=True,
)
flags.DEFINE_integer("run_seed", default=None, help="Seed for the run", required=True)
flags.DEFINE_string(
    "runs_dir",
    default=None,
    help="The root directory to (recursively) load the runs from",
    required=True,
)
flags.DEFINE_string(
    "out_dir",
    default=None,
    help="Directory for storing the experiment files",
    required=True,
)
flags.DEFINE_integer(
    "env_seed",
    default=None,
    help="Environment seed for resetting episodes",
    required=False,
)
flags.DEFINE_integer(
    "num_episodes",
    default=None,
    help="Number of evaluation episodes",
    required=False,
)
flags.DEFINE_integer(
    "buffer_size", default=1000, help="Number of transitions to store", required=False
)


def main(config: FlagValues):
    out_dir = os.path.join(config.out_dir, config.exp_name)
    os.makedirs(out_dir, exist_ok=True)

    num_runs = 0
    dat_content = ""
    for root, _, filenames in os.walk(config.runs_dir):
        for filename in filenames:
            if filename != "config.json":
                continue

            num_runs += 1
            run_path = root
            save_id = os.path.basename(os.path.abspath(os.path.join(root, os.pardir)))
            save_path = os.path.join(
                out_dir, f"{save_id}-{os.path.basename(root)}.gzip"
            )
            dat_content += (
                "export buffer_size={} num_episodes={} env_seed={} run_seed={} ".format(
                    config.buffer_size,
                    config.num_episodes,
                    config.env_seed,
                    config.run_seed,
                )
            )
            dat_content += "save_path={} run_path={}\n".format(save_path, run_path)
    with open(
        os.path.join(f"./export-generate_expert_data-{config.exp_name}.dat"), "w+"
    ) as f:
        f.writelines(dat_content)


if __name__ == "__main__":
    jax.config.config_with_absl()

    def _main(argv):
        """
        Generates experimental scripts for creating experts' data located in a directory.

        :param argv: the arguments provided by the user

        """
        del argv
        main(FLAGS)

    app.run(_main)
