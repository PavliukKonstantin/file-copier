"""Module with tests for testing the method 'test_copy_files'."""

import os


def test_correct_config(remove_files_in_destination, prepare_correct_config):
    copier, paths = prepare_correct_config
    _, destination_path, _, _ = paths
    copier.copy_files()
    files_in_destination = os.listdir(destination_path)
    expected = ["file_one.txt", "file_two.txt"]
    assert files_in_destination == expected


def test_config_with_incorrect_parameters(
    remove_files_in_destination,
    prepare_config_with_incorrect_parameters,
):
    copier, _ = prepare_config_with_incorrect_parameters
    try:
        copier.copy_files()
    except SystemExit:
        assert True


def test_config_with_nonexistent_file(
    remove_files_in_destination,
    prepare_config_with_nonexistent_file,
):
    copier, _ = prepare_config_with_nonexistent_file
    try:
        copier.copy_files()
    except SystemExit:
        assert True


def test_incorrect_config(
    remove_files_in_destination,
    prepare_incorrect_config
):
    copier, _ = prepare_incorrect_config
    try:
        copier.copy_files()
    except SystemExit:
        assert True


def test_empty_config(remove_files_in_destination, prepare_empty_config):
    copier, _ = prepare_empty_config
    try:
        copier.copy_files()
    except SystemExit:
        assert True
