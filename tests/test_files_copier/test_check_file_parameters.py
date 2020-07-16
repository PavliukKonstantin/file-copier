"""Module with tests for testing the method 'check_file_parameters'."""


def test_correct_config(prepare_correct_config):
    copier, paths = prepare_correct_config
    source_path, destination_path, _, _ = paths
    file_parameters = {
        "name": "file_one.txt",
        "source_path": source_path,
        "destination_path": destination_path,
    }
    check_result = copier.check_file_parameters(file_parameters)
    assert check_result is True


def test_config_with_incorrect_parameters(
    prepare_config_with_incorrect_parameters,
):
    copier, paths = prepare_config_with_incorrect_parameters
    source_path, _, _, _ = paths
    file_parameters = {
        "name": "file_three.txt",
        "source_path": source_path,
    }
    check_result = copier.check_file_parameters(file_parameters)
    assert check_result is False


def test_config_with_nonexistent_file(prepare_config_with_nonexistent_file):
    copier, paths = prepare_config_with_nonexistent_file
    source_path, destination_path, _, _ = paths
    file_parameters = {
        "name": "file_four.txt",
        "source_path": source_path,
        "destination_path": destination_path,
    }
    check_result = copier.check_file_parameters(file_parameters)
    assert check_result is False


def test_incorrect_config(prepare_incorrect_config):
    copier, paths = prepare_incorrect_config
    source_path, destination_path, _, _ = paths
    file_parameters = {
        "name": "file_one.txt",
        "asdasd": source_path,
        "zxczxc": destination_path,
    }
    check_result = copier.check_file_parameters(file_parameters)
    assert check_result is False


def test_empty_config(prepare_empty_config):
    copier, _ = prepare_empty_config
    file_parameters = {}
    check_result = copier.check_file_parameters(file_parameters)
    assert check_result is False
