import os
import git
import yaml
import argparse
import hashlib
import io
import tempfile
import zipfile
import shutil


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
        print("Bad config! Please, add list of repositories.")


def clone_repos():
    temp_dir = tempfile.TemporaryDirectory()

    repos = _get_repos_list()
    for rep in repos:
        git.Git(temp_dir.name).clone(rep.rstrip())

    dir_list = os.listdir(temp_dir.name)

    for directory in dir_list:
        shutil.move(temp_dir.name + "/" + directory, _get_save_path())


def main():
    clone_repos()


if __name__ == "__main__":
    main()
