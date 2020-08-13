import os

import pytest

from files_copier.copier import FilesCopier


def get_current_path() -> str:
    """Get the current path of the working directory."""
    return os.path.dirname(os.path.abspath(__file__))


def get_source_path(current_path: str) -> str:
    """Get the source directory path of the copied test files."""
    return os.path.join(current_path, "source")


def get_destination_path(current_path: str) -> str:
    """Get the destination directory path of the copied test files."""
    return os.path.join(current_path, "destination")


def get_configs_path(current_path: str) -> str:
    """Get the directory path of the test configuration files location."""
    return os.path.join(current_path, "configs")


def get_logs_path(current_path: str) -> str:
    """Get log recording directory path."""
    return os.path.join(current_path, "logs")


def get_paths_for_test(test_name: str) -> tuple:
    """Get all the necessary ways to conduct testing.

    Args:
        test_name (str): Name of the test

    Returns:
        Tuple of paths (source, destination, config file, log file).
    """
    current_path = get_current_path()
    source_path = get_source_path(current_path)
    destination_path = get_destination_path(current_path)
    configs_path = get_configs_path(current_path)
    logs_path = get_logs_path(current_path)
    config_file_path = os.path.join(configs_path, f"{test_name}.xml")
    log_file_path = os.path.join(logs_path, f"{test_name}.log")
    return (
        source_path,
        destination_path,
        config_file_path,
        log_file_path,
    )


def create_directory(path: str) -> None:
    """Create directory if it is doesn't exist."""
    if not os.path.isdir(path):
        os.mkdir(path)


def write_file(file_path: str, text: str = "") -> None:
    """Write text in file."""
    with open(file_path, "w") as file:
        file.write(text)


def format_config_text(config: str) -> str:
    """Delete four spaces at the beginning of each line."""
    lines = config.split("\n")
    lines = ((line, line[4:])[line.startswith(" ")] for line in lines)
    return "\n".join(lines)


def create_file(file_path: str, text: str = "") -> None:
    """Create a file and write text to it."""
    create_directory(os.path.dirname(file_path))
    write_file(file_path, text)


def create_copied_files() -> None:
    """Create files to be copied during testing."""
    current_path = get_current_path()
    source_path = get_source_path(current_path)
    file_one = os.path.join(source_path, "file_one.txt")
    file_two = os.path.join(source_path, "file_two.txt")
    file_three = os.path.join(source_path, "file_three.txt")
    files_paths = (file_one, file_two, file_three)
    for file_path in files_paths:
        create_file(file_path, os.path.basename(file_path))


def create_files_for_test(
    config_text: str,
    config_file_path: str,
    log_file_path: str,
) -> None:
    """Create all required files for testing."""
    config_text = format_config_text(config_text)
    create_file(config_file_path, config_text)
    create_file(log_file_path)
    create_copied_files()


@pytest.fixture()
def remove_files_in_destination() -> None:
    """Remove all files in destination directory."""
    destination_path = get_destination_path(get_current_path())
    removed_files = os.listdir(destination_path)
    for removed_file in removed_files:
        file_path = os.path.join(destination_path, removed_file)
        os.remove(file_path)


@pytest.fixture()
def prepare_correct_config() -> tuple:
    """To prepare the test.

    Prepare for the test with the correct configuration file
    and the correct configuration parameters.
    """
    paths = get_paths_for_test("correct_config")
    source_path, destination_path, config_file_path, log_file_path = paths

    config_text = f"""<?xml version="1.0"?>

    <files>
        <file>
            <name>file_one.txt</name>
            <source_path>{source_path}</source_path>
            <destination_path>{destination_path}</destination_path>
        </file>

        <file>
            <name>file_two.txt</name>
            <source_path>{source_path}</source_path>
            <destination_path>{destination_path}</destination_path>
        </file>

    </files>"""
    create_files_for_test(config_text, config_file_path, log_file_path)
    return FilesCopier(config_file_path, log_file_path), paths


@pytest.fixture()
def prepare_config_with_incorrect_parameters() -> tuple:
    """To prepare the test.

    Prepare for the test with the correct configuration file
    and the incorrect configuration parameters.
    """
    paths = get_paths_for_test("config_with_incorrect_parameters")
    source_path, _, config_file_path, log_file_path = paths

    config_text = f"""<?xml version="1.0"?>

    <files>
        <file>
            <name>file_three.txt</name>
            <source_path>{source_path}</source_path>
        </file>

    </files>"""
    create_files_for_test(config_text, config_file_path, log_file_path)
    return FilesCopier(config_file_path, log_file_path), paths


@pytest.fixture()
def prepare_config_with_nonexistent_file() -> tuple:
    """To prepare the test.

    Prepare for the test with the correct configuration file
    and the correct configuration parameters,
    but a file defined in the configuration doesn't exist.
    """
    paths = get_paths_for_test("config_with_nonexistent_file")
    source_path, destination_path, config_file_path, log_file_path = paths

    config_text = f"""<?xml version="1.0"?>

    <files>
        <file>
            <name>file_four.txt</name>
            <source_path>{source_path}</source_path>
            <destination_path>{destination_path}</destination_path>
        </file>

    </files>"""
    create_files_for_test(config_text, config_file_path, log_file_path)
    return FilesCopier(config_file_path, log_file_path), paths


@pytest.fixture()
def prepare_incorrect_config() -> tuple:
    """To prepare the test.

    Prepare to run the test with a configuration file that has a syntax error.
    """
    paths = get_paths_for_test("incorrect_config")
    _, _, config_file_path, log_file_path = paths

    config_text = """<?xml version="1.0"?>

    <"""
    create_files_for_test(config_text, config_file_path, log_file_path)
    return FilesCopier(config_file_path, log_file_path), paths


@pytest.fixture()
def prepare_empty_config() -> tuple:
    """To prepare the test.

    Prepare to run a test with an empty configuration file.
    """
    paths = get_paths_for_test("empty_config")
    _, _, config_file_path, log_file_path = paths
    config_text = """ """
    create_files_for_test(config_text, config_file_path, log_file_path)
    return FilesCopier(config_file_path, log_file_path), paths
