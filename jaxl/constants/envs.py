CONST_ENV_CONFIG = "env_config"
CONST_ENV_TYPE = "env_type"

CONST_DM_CONTROL = "dm_control"
CONST_GYM = "gym"

VALID_ENV_TYPE = [CONST_DM_CONTROL, CONST_GYM]


CONST_BASIS_POLYNOMIAL = "polynomial"

VALID_BASIS_FUNCTION = [CONST_BASIS_POLYNOMIAL]

CONST_MULTITASK_MNIST_FINEGRAIN = "multitask_mnist_finegrain"
CONST_STRATIFIED_MULTITASK_MNIST_FINEGRAIN = "stratified_multitask_mnist_finegrain"
CONST_MULTITASK_MNIST_RANDOM_BINARY = "multitask_mnist_random_binary"
VALID_MNIST_TASKS = [
    CONST_MULTITASK_MNIST_FINEGRAIN,
    CONST_STRATIFIED_MULTITASK_MNIST_FINEGRAIN,
    CONST_MULTITASK_MNIST_RANDOM_BINARY,
]


CONST_MULTITASK_TOY_REGRESSION = "multitask_toy_regression"
CONST_MULTITASK_ND_LINEAR_REGRESSION = "multitask_nd_linear_regression"
CONST_MULTITASK_ND_LINEAR_CLASSIFICATION = "multitask_nd_linear_classification"
CONST_MULTITASK_ND_RANDOM_CLASSIFICATION = "multitask_nd_random_classification"
CONST_MNIST = "mnist"
CONST_ONE_HOT_CLASSIFICATION = "one_hot_classification"
VALID_DATASET = [
    CONST_MULTITASK_TOY_REGRESSION,
    CONST_MULTITASK_ND_LINEAR_REGRESSION,
    CONST_MULTITASK_ND_LINEAR_CLASSIFICATION,
    CONST_MULTITASK_ND_RANDOM_CLASSIFICATION,
    CONST_MNIST,
    CONST_ONE_HOT_CLASSIFICATION,
]
