import itertools
import multiprocessing
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd

# import torch
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, DictConfig, OmegaConf
from src import constants

"""

@dataclass
class ModeConfig:
    train: bool = MISSING
    batch_size: int = MISSING
    date_range: List[str] = MISSING


@dataclass
class TrainConfig(ModeConfig):
    epochs: int = MISSING
    learning_rate: float = MISSING
    optimiser: str = MISSING
    loss_fn: str = MISSING
    test_metric: str = MISSING
    checkpoint_freq: int = MISSING
    val_interval: float = MISSING
    log_steps: int = MISSING
    fine_tune: bool = MISSING
    mc_dropout: bool = MISSING
    mc_dropout_iters: int = MISSING


@dataclass
class TestConfig(ModeConfig):
    pass


@dataclass
class ModelConfig:
    num_layers: int = MISSING
    type: str = MISSING


@dataclass
class LSTMConfig(ModelConfig):
    bidirectional: bool = MISSING
    hidden_units: int = MISSING
    dropout_rate: float = MISSING


@dataclass
class DatasetConfig:
    data_dir: Optional[str] = MISSING
    features: Dict[str, Any] = MISSING
    num_features: int = MISSING
    seq_length: int = MISSING
    train_test_split: str = MISSING
    basins_frac: float = MISSING
    shuffle: bool = MISSING
    num_workers: int = MISSING


@dataclass
class ConfigClass:
    mode: ModeConfig = MISSING
    model: ModelConfig = MISSING
    dataset: DatasetConfig = DatasetConfig()
    cuda: bool = MISSING
    parallel_engine: Optional[str] = MISSING
    precision: int = MISSING
    gpus: int = MISSING
    seed: int = MISSING
    run_name: str = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=ConfigClass)
cs.store(group="mode", name="train", node=TrainConfig)
cs.store(group="mode", name="test", node=TestConfig)
cs.store(group="model", name="lstm", node=LSTMConfig)


def validate_config(cfg: DictConfig) -> DictConfig:
    if cfg.run_name is None:
        raise TypeError("The `run_name` argument is mandatory.")
    if not set(cfg.dataset.features.keys()).issubset(set(constants.DATASET_KEYS)):
        raise ValueError(
            f"Keys in dataset.features must be from {constants.DATASET_KEYS}."
        )
    if not set(itertools.chain(*cfg.dataset.features.values())).issubset(
        set(constants.ALL_FEATURES)
    ):
        raise ValueError(
            "Feature names must be valid and non-timeseries features must not contain NaNs."
        )
    cfg.dataset.num_features = sum([len(x) for x in cfg.dataset.features.values()])
    # Set data_dir
    cfg.dataset.data_dir = os.path.join(constants.SRC_PATH, "data")
    # Validate train_test_split and date_range
    try:
        pd.Timestamp(cfg.dataset.train_test_split)
        [pd.Timestamp(date) for date in cfg.mode.date_range]
    except ValueError:
        print(
            "The parameters `dataset.train_test_split` and `mode.date_range` must be valid dates."
        )
    # Validate seq_length
    if cfg.dataset.seq_length <= 0:
        raise ValueError("The parameter `dataset.seq_length` must be > 0.")
    # Validate basins_frac
    if not 0.0 <= cfg.dataset.basins_frac <= 1.0:
        raise ValueError(
            f"The basins fraction {cfg.dataset.basins_frac} must be in the range [0, 1]."
        )
    if cfg.precision != 16 and cfg.precision != 32:
        raise ValueError(f"The precision {cfg.precision} must be either 16 or 32.")
    # Make sure num_workers isn't too high.
    core_count = multiprocessing.cpu_count()
    if cfg.dataset.num_workers > core_count * 2:
        cfg.dataset.num_workers = core_count
    if not cfg.cuda:
        cfg.gpus = 0
    if cfg.gpus <= 1:
        cfg.parallel_engine = None
    cfg.gpus = min(torch.cuda.device_count(), cfg.gpus)

    print("----------------- Options ---------------")
    print(OmegaConf.to_yaml(cfg))
    print("----------------- End -------------------")
    return cfg

"""
