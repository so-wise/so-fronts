# Place all your constants here
import os

# Note: constants should be UPPER_CASE
constants_path = os.path.realpath(__file__)
SRC_PATH = os.path.dirname(constants_path)
PROJECT_PATH = os.path.dirname(SRC_PATH)
DATA_PATH = os.path.join(PROJECT_PATH, "nc")

BSOSE_PATH = os.path.join("/Users", "simon", "bsose_monthly")
VAR_NAME_LIST = ["SALT", "THETA"]
SALT_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Salt.nc")
THETA_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Theta.nc")
VVEL_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Vvel.nc")
UVEL_FILE = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Uvel.nc")

Z_COORD = "Z"
Y_COORD = "YC"
X_COORD = "XC"
DEPTH_NAME = "Depth"
USELESS_LIST = ["iter", "Depth", "rA", "drF", "hFacC"]
RUN_NAME = "001"  # TODO --> Make all Data and Figures include RUN_NAME
FEATURES_D = {"THETA": "THETA", "SALT": "SALT"}
DIM_LIST = []
TIME_NAME = "time"
INTERP_FILE_NAME = os.path.join(DATA_PATH, "interp.nc")
