from torch.utils.data import Dataset
from types import SimpleNamespace
from typing import Callable, Dict, Any

from jaxl.constants import *
from jaxl.datasets.basis_regression import (
    MultitaskFixedBasisRegression1D,
)
from jaxl.datasets.wrappers import *

import chex
import numpy as np


"""
Getters for the datasets.
XXX: Feel free to add new components as needed.
"""


def get_basis(dataset_kwargs: SimpleNamespace) -> Callable[..., chex.Array]:
    """
    Gets a basis function.

    :param dataset_config: the dataset configuration
    :type dataset_config: SimpleNamespace
    :return: the basis function
    :rtype: Callable[..., chex.Array]
    """
    assert (
        dataset_kwargs.basis in VALID_BASIS_FUNCTION
    ), f"{dataset_kwargs.basis} is not supported (one of {VALID_BASIS_FUNCTION})"

    if dataset_kwargs.basis == CONST_BASIS_POLYNOMIAL:

        def polynomial_basis(x):
            return x ** np.arange(dataset_kwargs.degree + 1)

        return polynomial_basis
    else:
        raise ValueError(
            f"{dataset_kwargs.basis} is invalid (one of {VALID_BASIS_FUNCTION})"
        )


def get_dataset(
    dataset_config: SimpleNamespace,
    seed: int,
) -> Dataset:
    """
    Gets a dataset.

    :param dataset_config: the dataset configuration
    :param seed: the seed to generate the dataset
    :type dataset_config: SimpleNamespace
    :type seed: int
    :return: the dataset
    :rtype: Dataset
    """
    assert (
        dataset_config.dataset_name in VALID_DATASET
    ), f"{dataset_config.dataset_name} is not supported (one of {VALID_DATASET})"

    dataset_kwargs = dataset_config.dataset_kwargs
    if dataset_config.dataset_name == CONST_MULTITASK_TOY_REGRESSION:
        basis = get_basis(dataset_kwargs=dataset_kwargs)
        dataset = MultitaskFixedBasisRegression1D(
            num_sequences=dataset_kwargs.num_sequences,
            sequence_length=dataset_kwargs.sequence_length,
            basis=basis,
            seed=seed,
            noise=dataset_kwargs.noise,
            params_bound=dataset_kwargs.params_bound,
        )
    else:
        raise ValueError(
            f"{dataset_config.dataset_name} is not supported (one of {VALID_DATASET})"
        )

    if hasattr(dataset_config, CONST_DATASET_WRAPPER):
        if dataset_config.dataset_wrapper.type == "FixedLengthTrajectoryDataset":
            dataset = FixedLengthTrajectoryDataset(
                dataset, dataset_config.dataset_wrapper.kwargs.sample_seq_len
            )
        elif dataset_config.dataset_wrapper.type == "ContextDataset":
            dataset = ContextDataset(
                dataset,
                dataset_config.dataset_wrapper.kwargs.context_len,
                dataset_config.dataset_wrapper.kwargs.skip_step,
            )

    return dataset