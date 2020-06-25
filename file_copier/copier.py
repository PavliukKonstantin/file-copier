"""[summary].

Returns:
    [type]: [description]
"""

import xml.etree.ElementTree as ET
import sys
import os
import shutil
import time
import logging


# TODO think about how do this better
# create INFO logger for file
f_logger = logging.getLogger("file_INFO")
f_logger.setLevel(logging.INFO)
f_log = logging.FileHandler("copier.log")
f_formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
f_log.setFormatter(f_formatter)
f_logger.addHandler(f_log)

# create INFO logger for console
c_logger = logging.getLogger("console_INFO")
c_logger.setLevel(logging.INFO)
c_log = logging.StreamHandler()
c_formatter = logging.Formatter("%(levelname)s: %(message)s")
c_log.setFormatter(c_formatter)
c_logger.addHandler(c_log)


def get_file_params(files):
    return files.values()


def get_file_name(file: dict):
    """Get file name.

    Args:
        file (dict): File parameters

    Returns:
        str: File name
    """
    return file.get("name")


def get_source_path(file: dict):
    """Get file source path.

    Args:
        file (dict): File parameters

    Returns:
        str: File source path
    """
    return file.get("source_path")


def get_destination_path(file: dict):
    """Get file destination path.

    Args:
        file (dict): File parameters

    Returns:
        str: File destination path
    """
    return file.get("destination_path")


def check_source_path(source_path):
    return os.access(source_path, os.R_OK)


def check_copied_file(abs_path):
    return os.access(abs_path, os.R_OK)


def check_destination_path(destination_path):
    return os.access(destination_path, os.W_OK)


def get_abspath_to_file(source_path, file_name):
    return os.path.join(source_path, file_name)


def check_file_params(file_params: dict):
    file_name = get_file_name(file_params)
    source_path = get_source_path(file_params)
    destination_path = get_destination_path(file_params)
    if not(file_name and source_path and destination_path):
        return False

    source_is_ok = check_source_path(source_path)
    file_is_ok = check_copied_file(get_abspath_to_file(source_path, file_name))
    destination_is_ok = check_destination_path(destination_path)
    params_is_correct = bool(source_is_ok and file_is_ok and destination_is_ok)

    return params_is_correct


def get_root_config(config: str = "config.xml"):
    try:
        tree = ET.parse(config)
    except ET.ParseError:
        abs_path = os.path.abspath(config)
        text = "Configuration file - '{0}' is not correct".format(abs_path)
        f_logger.error(text)
        c_logger.error(text)
        return None
    except FileNotFoundError:
        abs_path = os.path.abspath(config)  # TODO think about it
        text = "Configuration file - '{0}' doesn't exist".format(abs_path)
        f_logger.error(text)
        c_logger.error(text)
        return None
    return tree.getroot()


def get_files_from_conf(config: str = "config.xml"):
    root = get_root_config(config)
    # TODO think about it!!!
    if root is None:
        return None
    files = {}
    for num, file in enumerate(root.findall("file")):
        file_params = {}
        for tag in list(file):
            file_params[tag.tag] = tag.text
        if check_file_params(file_params):
            files["File{0}".format(num)] = file_params
        else:
            # text = ("Wrong parameters in config for "
            #         "file - {0}".format(file_params))
            text = ("File with these parameters doesn't exist - "
                    "{0}".format(file_params))
            f_logger.error(text)
            c_logger.error(text)
    if not files:
        text = "Config - {0} haven't files for copy". format(config)
        f_logger.error(text)
        c_logger.error(text)
    return files


def copy_file(abspath_to_file: str, destination_path: str) -> None:
    try:
        sys.stdout.write("\033[2K")  # this code clear line
        shutil.copy(abspath_to_file, destination_path)
        text = "File - '{0}' successfully copied in -> '{1}'".format(
            abspath_to_file,
            destination_path
        )
        f_logger.info(text)
        c_logger.info(text)
    # except FileNotFoundError:
    except OSError:
        sys.stdout.flush()
        text = "File - '{0}' doesn't copied".format(abspath_to_file)
        f_logger.error(text)
        c_logger.error(text)


def progress(
        count: int,
        total: int,
        status: str = '',
        bar_len: int = 60) -> None:
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "{0}{1}".format("=" * filled_len, "-" * (bar_len - filled_len))

    fmt = "[{0}] {1}{2} ...{3}\r".format(bar, percents, "%", status)
    # print("\b" * len(fmt), end="")
    sys.stdout.write(fmt)
    sys.stdout.flush()


def copy_files(config: str = "config.xml") -> None:
    text = "Copying started"
    f_logger.info(text)
    c_logger.info(text)

    copied_files = get_files_from_conf(config)
    if not copied_files:
        return None
    for num, file in enumerate(get_file_params(copied_files)):
        source_path = get_source_path(file)
        file_name = get_file_name(file)
        destination_path = get_destination_path(file)
        abspath_to_file = get_abspath_to_file(source_path, file_name)

        progress(
            num,
            len(copied_files),
            status="Copying - '{0}'".format(file_name)
        )
        time.sleep(2)  # special for progress bar visualize
        copy_file(abspath_to_file, destination_path)
    text = "Copying completed"
    f_logger.info(text)
    c_logger.info(text)


if __name__ == "__main__":
    copy_files()
