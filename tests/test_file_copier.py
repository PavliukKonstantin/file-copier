from file_copier.copier import Copier
import os


# def test_version():
#     assert __version__ == '0.1.0'


# class PreparationForTests():

def create_directories():
    # TODO think about os.getcwd()
    current_path = os.getcwd()
    source_path = os.path.join(current_path, "source")
    try:
        os.mkdir(source_path)
        print("Directory - '{0}' was created".format(source_path))
    except FileExistsError:
        print("Directory - '{0}' is already exist".format(source_path))

    destination_path = os.path.join(current_path, "destination")
    try:
        os.mkdir(destination_path)
        print("Directory - '{0}' was created".format(destination_path))
    except FileExistsError:
        print("Directory - '{0}' is already exist".format(destination_path))
    return None


# TODO create files in "source"
def create_copied_files():
    # TODO think about os.getcwd()
    current_path = os.getcwd()
    source_path = os.path.join(current_path, "source")
    file_one = os.path.join(source_path, "file_one.txt")
    file_two = os.path.join(source_path, "file_two.txt")
    with open(file_one, "w") as file:
        file.write(os.path.basename(file_one))
    with open(file_two, "w") as file:
        file.write(os.path.basename(file_two))


# TODO create correct config with abspath to files in "source"
def create_correct_config():
    current_path = os.getcwd()
    source_path = os.path.join(current_path, "source")
    destination_path = os.path.join(current_path, "destination")
    file_one = "file_one.txt"
    file_two = "file_two.txt"

    # TODO this is ugly, fix it
    config = """<?xml version="1.0"?>

    <files>
        <file>
            <name>{file_one}</name>
            <source_path>{source_path}</source_path>
            <destination_path>{destination_path}</destination_path>
        </file>

        <file>
            <name>{file_two}</name>
            <source_path>{source_path}</source_path>
        </file>

        <file>
            <name>file_tree.txt</name>
            <source_path>{source_path}</source_path>
            <destination_path>{destination_path}</destination_path>
        </file>
    </files>""".format(
        file_one=file_one,
        file_two=file_two,
        source_path=source_path,
        destination_path=destination_path,
    )
    lines = config.split("\n")
    lines = ((line, line[4:])[line.startswith(" ")] for line in lines)
    config = "\n".join(lines)
    with open("correct_config.xml", "w") as file:
        file.write(config)


def create_uncorrect_config():
    # TODO this is ugly, fix it
    config = """<?xml version="1.0"?>

    <"""
    lines = config.split("\n")
    lines = ((line, line[4:])[line.startswith(" ")] for line in lines)
    config = "\n".join(lines)
    with open("uncorrect_config.xml", "w") as file:
        file.write(config)


# TODO prapare config files
# 1 normal config file
# 1 config file with syntax error
# for normal config:
#   1 file with correct parameters
#   1 file with uncorrect parameters
#   1 file with correct parameters, but file not exist

# create_directories()
# create_copied_files()
create_correct_config()
create_uncorrect_config()

# TODO test_get_root_config():
#   if config correct
#   if config uncorrect
#   if config not_exist
# def test_get_root_config():
#     pass


# TODO test_get_file_from_conf():

# if __name__ = "__main__":
#     pass
