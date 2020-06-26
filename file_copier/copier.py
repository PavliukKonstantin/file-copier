"""[summary]

config_example
<?xml version="1.0"?>

<files>
    <file>
        <name>file_one.txt</name>
        <source_path>abspath</source_path>
        <destination_path>abspath</destination_path>
    </file>

    <file>
        <name>file_two.txt</name>
        <source_path>abs_path</source_path>
        <destination_path>abs_path</destination_path>
    </file>
</files>

    Returns:
        [type]: [description]
    """

import xml.etree.ElementTree as ET
import sys
import os
import shutil
import time
import logging


class Copier():

    def __init__(
        self,
        config_file: str = "config.xml",
        log_file: str = "copier.log"
    ) -> None:
        # init config
        self.config = config_file
        self.log_file = log_file

        # TODO think about how do this better
        # init logger for file
        self.f_logger = logging.getLogger("file_log")
        self.f_logger.setLevel(logging.INFO)
        self.f_log = logging.FileHandler(self.log_file)
        self.f_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s: %(message)s"
        )
        self.f_log.setFormatter(self.f_formatter)
        self.f_logger.addHandler(self.f_log)

        # init logger for console
        self.c_logger = logging.getLogger("console_log")
        self.c_logger.setLevel(logging.INFO)
        self.c_log = logging.StreamHandler()
        self.c_formatter = logging.Formatter("%(levelname)s: %(message)s")
        self.c_log.setFormatter(self.c_formatter)
        self.c_logger.addHandler(self.c_log)

    def get_file_params(self, files):
        return files.values()

    def get_file_name(self, file: dict):
        file_name = file.get("name")
        if file_name is None:
            return ""
        return file_name

    def get_source_path(self, file: dict):
        source_path = file.get("source_path")
        if source_path is None:
            return ""
        return source_path

    def get_destination_path(self, file: dict):
        destination_path = file.get("destination_path")
        if destination_path is None:
            return ""
        return destination_path

    def check_source_path(self, source_path):
        return os.access(source_path, os.R_OK)

    def check_copied_file(self, abs_path):
        return os.access(abs_path, os.R_OK)

    def check_destination_path(self, destination_path):
        return os.access(destination_path, os.W_OK)

    def get_abspath_to_file(self, source_path, file_name):
        return os.path.join(source_path, file_name)

    def check_file_params(self, file_params: dict):
        file_name = self.get_file_name(file_params)
        source_path = self.get_source_path(file_params)
        destination_path = self.get_destination_path(file_params)
        if not(file_name and source_path and destination_path):
            return False

        source_is_ok = self.check_source_path(source_path)
        file_is_ok = self.check_copied_file(
            self.get_abspath_to_file(source_path, file_name))
        destination_is_ok = self.check_destination_path(destination_path)
        params_is_correct = bool(
            source_is_ok
            and file_is_ok
            and destination_is_ok
        )

        return params_is_correct

    def get_root_config(self):
        try:
            tree = ET.parse(self.config)
        except ET.ParseError:
            abs_path = os.path.abspath(self.config)
            text = "Configuration file - '{0}' is not correct".format(abs_path)
            self.f_logger.error(text)
            self.c_logger.error(text)
            return None
        except FileNotFoundError:
            abs_path = os.path.abspath(self.config)  # TODO think about it
            text = "Configuration file - '{0}' doesn't exist".format(abs_path)
            self.f_logger.error(text)
            self.c_logger.error(text)
            return None
        return tree.getroot()

    def get_files_from_conf(self):
        root = self.get_root_config()
        # TODO think about it!!!
        if root is None:
            return None
        files = {}
        for num, file in enumerate(root.findall("file")):
            file_params = {}
            for tag in list(file):
                file_params[tag.tag] = tag.text
            if self.check_file_params(file_params):
                files["File{0}".format(num)] = file_params
            else:
                text = ("File with these parameters doesn't exist - "
                        "{0}".format(file_params))
                self.f_logger.error(text)
                self.c_logger.error(text)
        if not files:
            text = "Config - {0} haven't files for copy". format(self.config)
            self.f_logger.error(text)
            self.c_logger.error(text)
        return files

    def copy_file(self, abspath_to_file: str, destination_path: str) -> None:
        try:
            sys.stdout.write("\033[2K")  # clear last stdout line
            shutil.copy(abspath_to_file, destination_path)
            text = "File - '{0}' successfully copied in -> '{1}'".format(
                abspath_to_file,
                destination_path
            )
            self.f_logger.info(text)
            self.c_logger.info(text)
        # except FileNotFoundError:
        except OSError:
            sys.stdout.flush()
            text = "File - '{0}' doesn't copied".format(abspath_to_file)
            self.f_logger.error(text)
            self.c_logger.error(text)

    def progress(
            self,
            count: int,
            total: int,
            status: str = '',
            bar_len: int = 60) -> None:
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = "{0}{1}".format(
            "=" * filled_len, "-" * (bar_len - filled_len))

        fmt = "[{0}] {1}{2} ...{3}\r".format(bar, percents, "%", status)
        sys.stdout.write("\033[2K")  # clear last stdout line
        sys.stdout.write(fmt)
        sys.stdout.flush()

    def copy_files(self) -> None:
        text = "Copying started"
        self.f_logger.info(text)
        self.c_logger.info(text)

        copied_files = self.get_files_from_conf()
        if not copied_files:
            return None
        for num, file in enumerate(self.get_file_params(copied_files)):
            source_path = self.get_source_path(file)
            file_name = self.get_file_name(file)
            destination_path = self.get_destination_path(file)
            abspath_to_file = self.get_abspath_to_file(source_path, file_name)

            self.progress(
                num,
                len(copied_files),
                status="Copying - '{0}'".format(file_name)
            )
            time.sleep(1)  # special for progress bar visualize
            self.copy_file(abspath_to_file, destination_path)
        text = "Copying completed"
        self.f_logger.info(text)
        self.c_logger.info(text)


if __name__ == "__main__":
    copy = Copier()
    copy.copy_files()
