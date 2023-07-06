CONST_ENCODER_PREDICTOR = "encoder_predictor"
CONST_ENSEMBLE = "ensemble"
CONST_MLP = "mlp"

VALID_ARCHITECTURE = [CONST_ENCODER_PREDICTOR, CONST_ENSEMBLE, CONST_MLP]


CONST_DETERMINISTIC = "deterministic"
CONST_GAUSSIAN = "gaussian"
CONST_SOFTMAX = "softmax"
CONST_SQUASHED_GAUSSIAN = "squashed_gaussian"
VALID_POLICY_DISTRIBUTION = [
    CONST_DETERMINISTIC,
    CONST_GAUSSIAN,
    CONST_SOFTMAX,
    CONST_SQUASHED_GAUSSIAN,
]

CONST_ENCODER = "encoder"
CONST_MODEL = "model"
CONST_POLICY = "policy"
CONST_PREDICTOR = "predictor"
CONST_REPRESENTATION = "representation"
CONST_VF = "vf"

CONST_MIN_STD = "min_std"

DEFAULT_MIN_STD = 1e-7

CONST_RELU = "relu"
CONST_TANH = "tanh"
VALID_ACTIVATION = [CONST_RELU, CONST_TANH]
