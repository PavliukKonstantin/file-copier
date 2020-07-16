import logging
import os
import shutil
import sys
import time
from typing import Union
from xml.etree import ElementTree


class FilesCopier(object):
    """Copy files defined in xml config.

    This class contains methods for copying files whose copy options
    are defined in the configuration file. Before copying,
    the parameters are checked for correctness and the ability
    to read the file and the ability to write to the destination
    directory that determined in the config.

    config_example
    <?xml version="1.0"?>
    <files>
        <file>
            <name>file_one.txt</name>
            <source_path>path_to_source_directory</source_path>
            <destination_path>path_to_destination_directory</destination_path>
        </file>

        <file>
            <name>file_two.txt</name>
            <source_path>path_to_source_directory</source_path>
            <destination_path>path_to_destination_directory</destination_path>
        </file>
    </files>
    """

    def __init__(
        self,
        config_file_path: str,
        log_file_path: str,
    ) -> None:
        """Initialize attributes of class and loggers for file and console.

        Args:
            config_file_path (str): An absolute or relative path
                                    to the configuration file
            log_file_path (str): An absolute or relative path
                                 to the log file
        """
        self.config_file = config_file_path
        self.log_file = log_file_path

        # Init file logger.
        # Unique name is necessary for the correct operation of
        # several instances of the class in one module
        self.f_logger = logging.getLogger(f"File {str(self.__hash__())}")
        self.f_logger.setLevel(logging.DEBUG)
        self.f_log = logging.FileHandler(self.log_file)
        self.f_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s: %(message)s",
        )
        self.f_log.setFormatter(self.f_formatter)
        self.f_logger.addHandler(self.f_log)

        # Init console logger.
        # Unique name is necessary for the correct operation of
        # several instances of the class in one module
        self.c_logger = logging.getLogger(f"Console {str(self.__hash__())}")
        self.c_logger.setLevel(logging.INFO)
        self.c_log = logging.StreamHandler()
        self.c_formatter = logging.Formatter("%(levelname)s: %(message)s")
        self.c_log.setFormatter(self.c_formatter)
        self.c_logger.addHandler(self.c_log)

    def _log_error(self, text: str) -> None:
        """Log message on LoggerLevel.error."""
        self.f_logger.error(text)
        self.c_logger.error(text)

    def _log_info(self, text: str) -> None:
        """Log message on LoggerLevel.info."""
        self.f_logger.info(text)
        self.c_logger.info(text)

    def _get_file_name(self, file_parameters: dict) -> str:
        """Get file name for copied file."""
        file_name = file_parameters.get("name")
        if file_name is None:
            return ""
        return file_name

    def _get_source_path(self, file_parameters: dict) -> str:
        """Get the source directory path."""
        source_path = file_parameters.get("source_path")
        if source_path is None:
            return ""
        return source_path

    def _get_destination_path(self, file_parameters: dict) -> str:
        """Get the destination directory path."""
        destination_path = file_parameters.get("destination_path")
        if destination_path is None:
            return ""
        return destination_path

    def _check_source_path(self, source_path: str) -> bool:
        """Check existence of the source directory."""
        return os.path.isdir(source_path)

    def _check_copied_file(self, file_path: str) -> bool:
        """Check the copied file.

        Checks the existence of the copied file and the permission to read.
        """
        source_path = os.path.dirname(file_path)
        if not self._check_source_path(source_path):
            return False
        try:
            copied_file = open(file_path, "r")
            copied_file.close()
        except OSError:
            return False
        return True

    def _check_destination_path(self, destination_path: str) -> bool:
        """Check the directory to which the file is copied.

        Check existence of destination directory and check write permission.
        If the directory doesn't exist, an attempt is made to create it.
        """
        if not os.path.isdir(destination_path):
            try:
                os.mkdir(destination_path)
                return True
            except OSError:
                return False
        tmp_file_path = os.path.join(destination_path, "tmp_file.txt")
        try:
            tmp_file = open(tmp_file_path, "w")
            tmp_file.close()
            os.remove(tmp_file_path)
        except OSError:
            return False
        return True

    def check_file_parameters(self, file_parameters: dict) -> bool:
        """Check that the copied file parameters exist and correct."""
        file_name = self._get_file_name(file_parameters)
        source_path = self._get_source_path(file_parameters)
        destination_path = self._get_destination_path(file_parameters)
        if all(
            (
                file_name,
                source_path,
                destination_path,
                self._check_copied_file(os.path.join(source_path, file_name)),
                self._check_destination_path(destination_path),
            )
        ):
            return True
        return False

    def get_root_of_config(self) -> Union[ElementTree.Element, None]:
        """Get root of configuration.

        Checks the configuration file for existence and correctness.
        Parsing the configuration in which the copied files are defined.
        """
        try:
            tree = ElementTree.parse(self.config_file)
        except ElementTree.ParseError:
            config_file_path = os.path.abspath(self.config_file)
            text = f"Configuration file is incorrect - {config_file_path}"
            self._log_error(text)
            return None
        except FileNotFoundError:
            config_file_path = os.path.abspath(self.config_file)
            text = (f"Configuration file doesn't exist - {config_file_path}")
            self._log_error(text)
            return None
        return tree.getroot()

    def get_copied_files_from_conf(self) -> list:
        """Get the parameters of the copied files from the configuration file.

        Parsing the configuration in which the copied files are defined.
        Also check the ability to copy each of files.
        """
        root = self.get_root_of_config()
        if root is None:
            return []
        files = []
        for file_tags in root.findall("file"):
            file_parameters = {}
            for tag in list(file_tags):
                file_parameters[tag.tag] = tag.text
            if self.check_file_parameters(file_parameters):
                files.append(file_parameters)
            else:
                text = (
                    "File with these parameters can't be copied - "
                    f"{file_parameters}"
                )
                self._log_error(text)
        if not files:
            text = f"Config doesn't have files for copy - {self.config_file}"
            self._log_error(text)
        return files

    def _copy_file(self, path_to_file: str, destination_path: str) -> None:
        """Copy one file."""
        try:
            sys.stdout.write("\033[2K")  # clear last stdout line
            shutil.copy2(path_to_file, destination_path)
            text = (
                f"File - {path_to_file} successfully "
                f"copied in -> {destination_path}"
            )
            self._log_info(text)
        except OSError:
            sys.stdout.flush()
            text = f"File doesn't copied - {path_to_file}"
            self._log_error(text)

    def _visualize_progress_bar(
        self,
        sequence_number: int,
        total_count: int,
        name_of_copied_file: str = "",
        bar_len: int = 50,
    ) -> None:
        """Display the progress of copying files in the console.

        Args:
            sequence_number (int): Sequence number of the copied files.
            total_count (int): Total number of the copied files.
            name_of_copied_file (str, optional):
                    Name of the copied file. Defaults to "".
            bar_len (int, optional): Length of progress bar. Defaults to 50.
        """
        filled_len = int(round(bar_len * sequence_number / float(total_count)))

        percents = round(100.0 * sequence_number / float(total_count), 1)
        completed_bar = "=" * filled_len
        uncompleted_bar = "-" * (bar_len - filled_len)
        progress_bar = f"{completed_bar}{uncompleted_bar}"

        progress_string = (
            f"[{progress_bar}] {percents}% "
            f"...{name_of_copied_file}\r"
        )
        sys.stdout.write("\033[2K")  # clear last stdout line
        sys.stdout.write(progress_string)
        sys.stdout.flush()

    def copy_files(self) -> None:
        """Copy files."""
        self._log_info("Copying started")

        copied_files = self.get_copied_files_from_conf()
        if not copied_files:
            text = "Copying is completed. Nothing is copied."
            self._log_info(text)
            raise SystemExit
        for num, copied_file in enumerate(copied_files):
            source_path = self._get_source_path(copied_file)
            file_name = self._get_file_name(copied_file)
            destination_path = self._get_destination_path(copied_file)
            path_to_file = os.path.join(source_path, file_name)

            self._visualize_progress_bar(
                num,
                len(copied_files),
                name_of_copied_file=f"Copying - {file_name}"
            )
            time.sleep(1)  # special for progress bar visualize
            self._copy_file(path_to_file, destination_path)

        self._log_info("Copying is completed")


if __name__ == "__main__":
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config.xml",
    )
    log_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "files_copier.log",
    )
    copier = FilesCopier(config_path, log_path)
    copier.copy_files()
