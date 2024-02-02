from torch.utils.data import Dataset
from types import SimpleNamespace
from typing import Tuple

from jaxl.constants import (
    VALID_MNIST_TASKS,
    CONST_MULTITASK_MNIST_FINEGRAIN,
    CONST_STRATIFIED_MULTITASK_MNIST_FINEGRAIN,
    CONST_MULTITASK_MNIST_RANDOM_BINARY,
)

import _pickle as pickle
import chex
import jax.random as jrandom
import numpy as np
import os
import torchvision.datasets as torch_datasets

import jaxl.transforms as jaxl_transforms


def construct_mnist(
    save_path: str,
    task_name: str = None,
    task_config: SimpleNamespace = None,
    train: bool = True,
) -> Dataset:
    """
    Constructs a customized MNIST dataset.

    :param save_path: the path to store the MNIST dataset
    :param task_name: the task to construct
    :param task_config: the task configuration
    :param train: the train split of the dataset
    :type save_path: str
    :type task_name: str:  (Default value = None)
    :type task_config: SimpleNamespace:  (Default value = None)
    :type train: bool:  (Default value = True)
    :return: Customized MNIST dataset
    :rtype: Dataset

    """
    assert (
        task_name is None or task_name in VALID_MNIST_TASKS
    ), f"{task_name} is not supported (one of {VALID_MNIST_TASKS})"
    target_transform = None

    if task_name is None:
        # By default, the MNIST task will be normalized to be between 0 to 1.
        return torch_datasets.MNIST(
            save_path,
            train=train,
            download=True,
            transform=jaxl_transforms.DefaultPILToImageTransform(),
            target_transform=target_transform,
        )
    elif task_name == CONST_MULTITASK_MNIST_FINEGRAIN:
        return MultitaskMNISTFineGrain(
            dataset=torch_datasets.MNIST(
                save_path,
                train=train,
                download=True,
                transform=jaxl_transforms.StandardImageTransform(),
                target_transform=target_transform,
            ),
            num_sequences=task_config.num_sequences,
            sequence_length=task_config.sequence_length,
            random_label=getattr(task_config, "random_label", False),
            save_path=task_config.save_path,
        )
    elif task_name == CONST_STRATIFIED_MULTITASK_MNIST_FINEGRAIN:
        return StratifiedMultitaskMNISTFineGrain(
            dataset=torch_datasets.MNIST(
                save_path,
                train=train,
                download=True,
                transform=jaxl_transforms.StandardImageTransform(),
                target_transform=target_transform,
            ),
            num_sequences=task_config.num_sequences,
            num_queries=task_config.num_queries,
            random_label=getattr(task_config, "random_label", False),
            save_path=task_config.save_path,
        )
    elif task_name == CONST_MULTITASK_MNIST_RANDOM_BINARY:
        return MultitaskMNISTRandomBinary(
            dataset=torch_datasets.MNIST(
                save_path,
                train=train,
                download=True,
                transform=jaxl_transforms.StandardImageTransform(),
                target_transform=target_transform,
            ),
            num_sequences=task_config.num_sequences,
            sequence_length=task_config.sequence_length,
            save_path=task_config.save_path,
        )
    else:
        raise ValueError(f"{task_name} is invalid (one of {VALID_MNIST_TASKS})")


class MultitaskMNISTFineGrain(Dataset):
    """
    The dataset contains multiple ND (fixed) linear classification problems.
    """

    def __init__(
        self,
        dataset: Dataset,
        num_sequences: int,
        sequence_length: int,
        seed: int = 0,
        random_label: bool=False,
        save_path: str = None,
    ):
        self._dataset = dataset
        self._sequence_length = sequence_length
        self._random_label = random_label

        if save_path is None or not os.path.isfile(save_path):
            (self.sample_idxes, self.label_map) = self._generate_data(
                dataset=dataset,
                num_sequences=num_sequences,
                random_label=random_label,
                seed=seed,
            )
            if save_path is not None:
                print("Saving to {}".format(save_path))
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                pickle.dump(
                    (self.sample_idxes, self.label_map),
                    open(save_path, "wb"),
                )
        else:
            print("Loading from {}".format(save_path))
            (self.sample_idxes, self.label_map) = pickle.load(
                open(save_path, "rb")
            )

    def _generate_data(
        self,
        dataset: Dataset,
        num_sequences: int,
        random_label: bool,
        seed: int,
    ) -> Tuple[chex.Array, chex.Array, chex.Array]:
        print("Generating Data")
        sample_key, label_key = jrandom.split(jrandom.PRNGKey(seed))
        sample_rng = np.random.RandomState(sample_key)
        label_rng = np.random.RandomState(label_key)

        sample_idxes = sample_rng.choice(
            np.arange(len(dataset)),
            size=(num_sequences, self._sequence_length)
        )


        label_map = np.tile(np.arange(self.output_dim[0]), reps=(num_sequences, 1))
        if random_label:
            label_map = np.apply_along_axis(label_rng.permutation, axis=1, arr=label_map)

        return sample_idxes, label_map

    @property
    def input_dim(self) -> chex.Array:
        return [*self._dataset.data[0].shape]

    @property
    def output_dim(self) -> chex.Array:
        return (10,)

    @property
    def sequence_length(self) -> int:
        return self._sequence_length

    def __len__(self):
        return len(self.sample_idxes)

    def __getitem__(self, idx):
        sample_idxes = self.sample_idxes[idx].tolist()
        inputs = self._dataset.transform(self._dataset.data[sample_idxes])
        labels = self.label_map[idx][self._dataset.targets[sample_idxes]]
        outputs = np.eye(self.output_dim[0])[labels]
        return (inputs, outputs)


class StratifiedMultitaskMNISTFineGrain(Dataset):
    """
    The dataset contains multiple ND (fixed) linear classification problems.
    """

    def __init__(
        self,
        dataset: Dataset,
        num_sequences: int,
        num_queries: int,
        seed: int = 0,
        random_label: bool=False,
        save_path: str = None,
    ):
        self._dataset = dataset

        _, counts = np.unique(dataset.targets, return_counts=True)
        self._min_num_per_class = np.min(counts)
        self._label_to_idx = np.vstack(
            [np.where(dataset.targets == class_i)[0][:self._min_num_per_class] for class_i in range(self.output_dim[0])]
        )
        self._num_queries = num_queries
        self._random_label = random_label

        if save_path is None or not os.path.isfile(save_path):
            (self.context_idxes, self.query_idxes, self.swap_idxes, self.label_map) = self._generate_data(
                dataset=dataset,
                num_sequences=num_sequences,
                random_label=random_label,
                seed=seed,
            )
            if save_path is not None:
                print("Saving to {}".format(save_path))
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                pickle.dump(
                    (self.context_idxes, self.query_idxes, self.swap_idxes, self.label_map),
                    open(save_path, "wb"),
                )
        else:
            print("Loading from {}".format(save_path))
            (self.context_idxes, self.query_idxes, self.swap_idxes, self.label_map) = pickle.load(
                open(save_path, "rb")
            )

    def _generate_data(
        self,
        dataset: Dataset,
        num_sequences: int,
        random_label: bool,
        seed: int,
    ) -> Tuple[chex.Array, chex.Array, chex.Array]:
        print("Generating Data")
        sample_key, label_key = jrandom.split(jrandom.PRNGKey(seed))
        sample_rng = np.random.RandomState(sample_key)
        label_rng = np.random.RandomState(label_key)

        query_idxes = sample_rng.choice(
            np.arange(len(dataset)),
            size=(num_sequences, self._num_queries)
        )

        context_idxes = sample_rng.choice(
            np.arange(self._min_num_per_class),
            size=(num_sequences, self.output_dim[0])
        )

        label_map = np.tile(np.arange(self.output_dim[0]), reps=(num_sequences, 1))

        swap_idxes = np.apply_along_axis(sample_rng.permutation, axis=1, arr=label_map)

        if random_label:
            label_map = np.apply_along_axis(label_rng.permutation, axis=1, arr=label_map)

        return context_idxes, query_idxes, swap_idxes, label_map

    @property
    def input_dim(self) -> chex.Array:
        return [*self._dataset.data[0].shape]

    @property
    def output_dim(self) -> chex.Array:
        return (10,)

    @property
    def num_queries(self) -> int:
        return self._num_queries

    def __len__(self):
        return len(self.query_idxes)

    def __getitem__(self, idx):
        context_idxes = self.context_idxes[idx]
        context_idxes = np.take_along_axis(self._label_to_idx, context_idxes[:, None], axis=1).flatten()
        context_inputs = self._dataset.transform(self._dataset.data[context_idxes])
        context_outputs = self.label_map[idx][self._dataset.targets[context_idxes]]

        context_inputs = context_inputs[self.swap_idxes[idx]]
        context_outputs = context_outputs[self.swap_idxes[idx]]
        context_outputs = np.eye(self.output_dim[0])[context_outputs]

        query_idxes = self.query_idxes[idx].tolist()
        queries = self._dataset.transform(self._dataset.data[query_idxes])
        labels = np.atleast_1d(self.label_map[idx][self._dataset.targets[query_idxes]])
        labels = np.eye(self.output_dim[0])[labels]

        return (context_inputs, context_outputs, queries, labels)


class MultitaskMNISTRandomBinary(Dataset):
    """
    The dataset contains multiple ND (fixed) linear classification problems.
    """

    def __init__(
        self,
        dataset: Dataset,
        num_sequences: int,
        sequence_length: int,
        seed: int = 0,
        save_path: str = None,
    ):
        self._dataset = dataset
        self._sequence_length = sequence_length

        if save_path is None or not os.path.isfile(save_path):
            self.sample_idxes, self.label_map = self._generate_data(
                dataset=dataset,
                num_sequences=num_sequences,
                seed=seed,
            )
            if save_path is not None:
                print("Saving to {}".format(save_path))
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                pickle.dump(
                    (self.sample_idxes, self.label_map),
                    open(save_path, "wb"),
                )
        else:
            print("Loading from {}".format(save_path))
            (self.sample_idxes, self.label_map) = pickle.load(
                open(save_path, "rb")
            )

    def _generate_data(
        self,
        dataset: Dataset,
        num_sequences: int,
        seed: int,
    ) -> Tuple[chex.Array, chex.Array, chex.Array]:
        sample_key, label_key = jrandom.split(jrandom.PRNGKey(seed))
        sample_rng = np.random.RandomState(sample_key)
        label_rng = np.random.RandomState(label_key)

        sample_idxes = sample_rng.choice(
            np.arange(len(dataset)),
            size=(num_sequences, self._sequence_length)
        )
        
        label_map = np.zeros((10,), dtype=np.int32)
        ones = label_rng.choice(
            np.arange(10),
            replace=False,
            size=(5,),
        )
        label_map[ones] = 1
        return sample_idxes, label_map

    @property
    def input_dim(self) -> chex.Array:
        return [*self._dataset.data[0].shape]

    @property
    def output_dim(self) -> chex.Array:
        return (10,)

    @property
    def sequence_length(self) -> int:
        return self._sequence_length

    def __len__(self):
        return len(self.sample_idxes)

    def __getitem__(self, idx):
        sample_idxes = self.sample_idxes[idx].tolist()
        inputs = self._dataset.transform(self._dataset.data[sample_idxes])
        outputs = np.eye(self.output_dim[0])[self.label_map[self._dataset.targets[sample_idxes]]]
        return (inputs, outputs)
