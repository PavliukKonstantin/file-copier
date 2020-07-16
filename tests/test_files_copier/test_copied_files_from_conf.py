"""Module with tests for testing the method 'test_copied_files_from_conf'."""


def test_correct_config(prepare_correct_config):
    copier, paths = prepare_correct_config
    files = copier.get_copied_files_from_conf()
    source_path, destination_path, _, _ = paths
    expected = [
        {
            "name": "file_one.txt",
            "source_path": source_path,
            "destination_path": destination_path,
        },
        {
            "name": "file_two.txt",
            "source_path": source_path,
            "destination_path": destination_path,
        },
    ]
    assert files == expected


def test_config_with_incorrect_parameters(
    prepare_config_with_incorrect_parameters,
):
    copier, _ = prepare_config_with_incorrect_parameters
    files = copier.get_copied_files_from_conf()
    expected = []
    assert files == expected


def test_config_with_nonexistent_file(prepare_config_with_nonexistent_file):
    copier, _ = prepare_config_with_nonexistent_file
    files = copier.get_copied_files_from_conf()
    expected = []
    assert files == expected


def test_incorrect_config(prepare_incorrect_config):
    copier, _ = prepare_incorrect_config
    files = copier.get_copied_files_from_conf()
    expected = []
    assert files == expected


def test_empty_config(prepare_empty_config):
    copier, _ = prepare_empty_config
    files = copier.get_copied_files_from_conf()
    expected = []
    assert files == expected
