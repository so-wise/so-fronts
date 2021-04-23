"""Constants.py program for storing paths and variables names."""

# Place all your constants here
import os
import numpy as np
import pathlib
from sys import platform

print("platform", platform)

# Note: constants should be UPPER_CASE

# Basic location defaults, to be referenced from here:
constants_path = os.path.realpath(__file__)
SRC_PATH = os.path.dirname(constants_path)
PROJECT_PATH = os.path.dirname(SRC_PATH)
DATA_PATH = os.path.join(PROJECT_PATH, "nc")
FIGURE_PATH = os.path.join(PROJECT_PATH, "report", "figures")
KO_PATH = os.path.join(SRC_PATH, "data", "kim_(&orsi)_altimetric_fronts")

# MAIN
MAIN_DIR: str = "/Users/simon/bsose_monthly/"
SALT: str = MAIN_DIR + "bsose_i106_2008to2012_monthly_Salt.nc"
THETA: str = MAIN_DIR + "bsose_i106_2008to2012_monthly_Theta.nc"

# Data directory on GWS
GWS_DATA_DIR = pathlib.Path("/gws/nopw/j04/ai4er/users/sdat2")

# Paths to different BSOSE-i106 files (unique to my machine):
if platform == "Linux" or platform == "linux":
    GEN_DATA_PATH = os.path.join(GWS_DATA_DIR, "bsose_data")
    BSOSE_PATH = os.path.join(GWS_DATA_DIR, "bsose_data", "bsose_salt_temp")

elif platform == "Darwin":
    BSOSE_PATH = os.path.join("/Users", "simon", "bsose_monthly")
    GEN_DATA_PATH = BSOSE_PATH

else:
    assert False

SALT_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Salt.nc")
THETA_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Theta.nc")
VVEL_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Vvel.nc")
UVEL_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Uvel.nc")

# COORDS within BSOSE-i106
Z_COORD: str = "Z"
D_COORD: str = "Depth"
Y_COORD: str = "YC"
X_COORD: str = "XC"
T_COORD: str = "time"

# COORDS created in my variables
P_COORD: str = "pair"
CLUST_COORD: str = "cluster"

# Particular names within BSOSE-i106
DEPTH_NAME: str = "Depth"
USELESS_LIST: list = ["iter", "Depth", "rA", "drF", "hFacC"]
VAR_NAME_LIST: list = ["SALT", "THETA"]
FEATURES_D: dict = {"THETA": "THETA", "SALT": "SALT"}

# Naming of intermediate files
INTERP_FILE_NAME = os.path.join(DATA_PATH, "interp.nc")

# Chosen hyperparameters in the model run:
RUN_NAME: str = "010"  # TODO --> Make all Data and Figures include RUN_NAME
SEED: int = int(RUN_NAME)  # TODO --> Make GMM training function take random seed.
np.random.seed(SEED)
MIN_DEPTH: float = 300  # m
MAX_DEPTH: float = 2000  # m
K_CLUSTERS: int = 5
D_PCS: int = 3
EXAMPLE_TIME_INDEX: int = 40  # the default time to go for.
EXAMPLE_Z_INDEX: int = 15
DEFAULT_NC: str = "~/pyxpcm_sithom/nc/i-metric-joint-k-5-d-3.nc"
