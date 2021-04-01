"""Constants.py program for storing paths and variables names."""

# Place all your constants here
import numpy as np
import os

# Note: constants should be UPPER_CASE

# Basic location defaults, to be referenced from here:

constants_path = os.path.realpath(__file__)
SRC_PATH = os.path.dirname(constants_path)
PROJECT_PATH = os.path.dirname(SRC_PATH)
DATA_PATH = os.path.join(PROJECT_PATH, "nc")
FIGURE_PATH = os.path.join(PROJECT_PATH, "report", "figures")
KO_PATH = os.path.join(SRC_PATH, "data", "kim_(&orsi)_altimetric_fronts")


# Paths to different BSOSE-i106 files (unique to my machine):

BSOSE_PATH = os.path.join("/Users", "simon", "bsose_monthly")
SALT_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Salt.nc")
THETA_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Theta.nc")
VVEL_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Vvel.nc")
UVEL_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Uvel.nc")


# COORDS within BSOSE-i106

Z_COORD = "Z"
Y_COORD = "YC"
X_COORD = "XC"
T_COORD = "time"

# COORDS created in my variables

P_COORD = "pair"
CLUST_COORD = "cluster"


# Particular names within BSOSE-i106

DEPTH_NAME = "Depth"
USELESS_LIST = ["iter", "Depth", "rA", "drF", "hFacC"]
VAR_NAME_LIST = ["SALT", "THETA"]
FEATURES_D = {"THETA": "THETA", "SALT": "SALT"}


# Naming of intermediate files

INTERP_FILE_NAME = os.path.join(DATA_PATH, "interp.nc")


# Chosen hyperparameters in the model run:

RUN_NAME = "010"  # TODO --> Make all Data and Figures include RUN_NAME
SEED = int(RUN_NAME)  # TODO --> Make GMM training function take random seed.
np.random.seed(SEED)
MIN_DEPTH = 300  # TODO --> make this feed the keyword argument defaults
MAX_DEPTH = 2000
K_CLUSTERS = 5
D_PCS = 3
