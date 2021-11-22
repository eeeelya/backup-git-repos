import os
import git
import yaml
import hashlib
import io
import tempfile
import zipfile
import shutil
import logging.config
from pathlib import Path

# LOGGING_CONFIG = {
#     # Set the preferred schema version.
#     "version": 1,
#     "formatters": {
#         "default": {
#             "format": "%(asctime)s - %(levelname)s :: %(name)s :: %(message)s",
#             # Use this string to format the creation time of the record.
#             "datefmt": "%Y-%m-%d--%H-%M-%S",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "default",
#             "stream": "ext://sys.stdout",
#         },
#         "logfile": {
#             "class": "logging.FileHandler",
#             "encoding": "utf-8",
#             "filename": "backup-git-repos.log",
#             "formatter": "default",
#             "mode": "at",
#         },
#     },
#     "loggers": {
#         "backup-git-repos": {
#             "handlers": ["console", "logfile"],
#         },
#     }
# }

# logging.config.dictConfig(config=LOGGING_CONFIG)
_logger = logging.getLogger("backup_git_repos")

SAVE_PATH = "."


def _get_settings_from_config():
    with io.open("config.yaml", mode="rt", encoding="utf-8") as stream_in:
        settings = yaml.safe_load(stream_in)
    return settings


SETTINGS = _get_settings_from_config()


def _get_save_path():
    return SETTINGS.get("save_path", SAVE_PATH)


def _get_repos_list():
    try:
        repos = SETTINGS["repos"]
        return repos
    except KeyError:
        _logger.error("Bad config! Please, add list of repositories.")
        exit()


def clone_repos():
    temp_dir = tempfile.TemporaryDirectory()

    repos = _get_repos_list()
    try:
        for rep in repos:
            git.Git(temp_dir.name).clone(rep.rstrip())
    except TypeError:
        _logger.error("List of repositories is empty!")

    dir_list = os.listdir(temp_dir.name)

    for directory in dir_list:
        if os.path.isdir(os.path.join(_get_save_path(), directory)):
            shutil.rmtree(os.path.join(_get_save_path(), directory))
        shutil.move(os.path.join(temp_dir.name, directory), _get_save_path())


def _calculate_hash_for_file(path, file):
    hash_sha1 = hashlib.sha1()
    with open(os.path.join(path, file), "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def get_files_with_hash():
    dir_list = os.listdir(_get_save_path())
    for directory in dir_list:
        path_to_dir = os.path.join(_get_save_path(), directory)
        if os.path.isdir(path_to_dir):
            with io.open(Path(path_to_dir).with_suffix('.txt'), mode="w", encoding="UTF-8") as stream_out:
                for path, dirs, files in os.walk(path_to_dir):
                    for file in files:
                        hash_sha1 = _calculate_hash_for_file(path, file)
                        stream_out.write(file + " - " + hash_sha1 + "\n")


def archive_repos():
    dir_list = os.listdir(_get_save_path())
    for directory in dir_list:
        path_to_dir = os.path.join(_get_save_path(), directory)
        if os.path.isdir(path_to_dir):
            archive = zipfile.ZipFile(Path(path_to_dir).with_suffix('.zip'), mode="w")
            for root, dirs, files in os.walk(path_to_dir):
                for file in files:
                    archive.write(os.path.join(root, file),
                                  os.path.relpath(os.path.join(root, file),
                                                  os.path.join(_get_save_path())))
            filename = Path(path_to_dir)
            archive.write(filename.with_suffix('.txt'),
                          os.path.relpath(filename.with_suffix('.txt'),
                                          os.path.join(_get_save_path())))


def main():
    clone_repos()
    get_files_with_hash()
    archive_repos()


if __name__ == "__main__":
    main()
