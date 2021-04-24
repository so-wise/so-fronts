"""Download the data from dropbox links.

'get_zip'  682.31512 s

'un_zip'  239.17872 s

'clean_up'  2.31065 s

'get_and_unzip'  923.80469 s

Example:
    Import statement::
        from src.data_loading.bsose_download import get_data

    Run statement::
        get_data()

"""
import os
import sys
import shutil
import requests

if sys.version_info >= (3, 8):
    import zipfile
else:
    import zipfile38 as zipfile
from tqdm import tqdm
import src.time_wrapper as twr
from src.constants import GEN_DATA_PATH


@twr.timeit
def get_and_unzip(direc: str, url: str, name: str) -> None:
    """Get the data and unzip it.

    Args:
        direc (str): directory to put the data in.
        url (str): url of the zip file.
        name (str): name of file.

    """

    write_path = os.path.join(direc, name)

    @twr.timeit
    def get_zip() -> None:
        req = requests.get(url, stream=True)
        with open(write_path, "wb") as file:
            for chunk in tqdm(req.iter_content(chunk_size=128)):
                file.write(chunk)

    @twr.timeit
    def un_zip() -> None:
        with zipfile.ZipFile(write_path, "r") as zip_ref:
            zip_ref.extractall(direc)

    @twr.timeit
    def clean_up() -> None:
        os.remove(write_path)
        mac_path = os.path.join(direc, "__MACOSX")
        if os.path.exists(mac_path):
            shutil.rmtree(mac_path)

    get_zip()
    un_zip()
    clean_up()


PREFIX = "https://www.dropbox.com/s/"
SUFFIX = "?raw=1"


def get_data() -> None:
    """Downloads data."""

    code = "tvflaeux4wwq6zq/"
    name = "bsose_salt_temp.zip"

    lol = [
        [
            str(GEN_DATA_PATH),
            [
                [
                    PREFIX + code + name + SUFFIX,
                    name,
                ],
            ],
        ],
    ]

    _get_data(lol)


def _get_data(lol: list) -> None:
    """Gets the data using lol.

    Args:
        lol (list): list of lists
    """
    for item in lol:
        direc = item[0]
        if not os.path.exists(direc):
            os.mkdir(direc)
        for pair in item[1]:
            url = pair[0]
            name = pair[1]
            full_direc = str(os.path.join(direc, os.path.splitext(pair[1])[0]))
            if not os.path.exists(full_direc):
                print("Dowloading " + full_direc)
                get_and_unzip(direc, url, name)
                print(full_direc + " created.")
            else:
                print(full_direc + " already exists, not going to redownload.")


if __name__ == "__main__":
    # python3 src/data_loading/bsose_download.py
    get_data()
