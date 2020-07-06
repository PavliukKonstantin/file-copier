"""Module with tests for testing the method 'test_get_root_of_config'."""

from xml.etree import ElementTree


def test_correct_config(prepare_correct_config):
    copier, _ = prepare_correct_config
    root = type(copier.get_root_of_config())
    assert root is ElementTree.Element


def test_config_with_incorrect_parameters(
    prepare_config_with_incorrect_parameters,
):
    copier, _ = prepare_config_with_incorrect_parameters
    root = type(copier.get_root_of_config())
    assert root is ElementTree.Element


def test_config_with_nonexistent_file(prepare_config_with_nonexistent_file):
    copier, _ = prepare_config_with_nonexistent_file
    root = type(copier.get_root_of_config())
    assert root is ElementTree.Element


def test_incorrect_config(prepare_incorrect_config):
    copier, _ = prepare_incorrect_config
    root = copier.get_root_of_config()
    assert root is None


def test_empty_config(prepare_empty_config):
    copier, _ = prepare_empty_config
    root = copier.get_root_of_config()
    assert root is None
