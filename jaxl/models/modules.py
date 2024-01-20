from flax import linen as nn
from typing import Callable, Sequence

import chex


class MLPModule(nn.Module):
    """Multilayer Perceptron."""

    # The number of hidden units in each hidden layer.
    layers: Sequence[int]
    activation: Callable
    output_activation: Callable

    @nn.compact
    def __call__(self, x: chex.Array) -> chex.Array:
        for layer in self.layers[:-1]:
            x = self.activation(nn.Dense(layer)(x))
        x = self.output_activation(nn.Dense(self.layers[-1])(x))
        return x
    

class CNNModule(nn.Module):
    """Convolutional layer."""

    # The number of hidden units in each hidden layer.
    features: Sequence[int]
    kernel_sizes: Sequence[Sequence[int]]
    activation: Callable

    @nn.compact
    def __call__(self, x: chex.Array) -> chex.Array:
        for feature, kernel_size in zip(self.features, self.kernel_sizes):
            x = self.activation(nn.Conv(feature, kernel_size)(x))
        return x


class GPTBlock(nn.Module):
    """GPT Block."""

    # : The number of attention heads
    num_heads: int

    # : The embedding dimensionality
    embed_dim: int

    @nn.compact
    def __call__(self, x: chex.Array) -> chex.Array:
        mask = nn.make_causal_mask(x[..., 0])
        x = x + nn.SelfAttention(self.num_heads)(nn.LayerNorm()(x), mask)
        normed_x = nn.gelu(nn.Dense(self.embed_dim)(nn.LayerNorm()(x)))
        x = x + nn.Dense(self.embed_dim)(normed_x)
        return x


class GPTModule(nn.Module):
    """GPT."""

    # : The number of GPT Blocks
    num_blocks: int

    # : The number of attention heads
    num_heads: int

    # : The embedding dimensionality
    embed_dim: int

    @nn.compact
    def __call__(self, x: chex.Array) -> chex.Array:
        for _ in range(self.num_blocks):
            x = GPTBlock(self.num_heads, self.embed_dim)(x)
        x = nn.LayerNorm()(x)
        return x
