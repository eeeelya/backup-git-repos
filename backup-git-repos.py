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
        shutil.rmtree(_get_save_path() + "/" + directory)
        shutil.move(temp_dir.name + "/" + directory, _get_save_path())


def _calculate_hash_for_file(path, file):
    hash_sha1 = hashlib.sha1()
    with open(path + "/" + file, "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def get_files_with_hash_for_repos():
    dir_list = os.listdir(_get_save_path())
    for directory in dir_list:
        if os.path.isdir(_get_save_path() + "/" + directory):
            with io.open(_get_save_path() + "/" + directory + ".txt", mode="w", encoding="UTF-8") as stream_out:
                for path, dirs, files in os.walk(_get_save_path() + "/" + directory):
                    for file in files:
                        hash_sha1 = _calculate_hash_for_file(path, file)
                        stream_out.write(file + " - " + hash_sha1 + "\n")

def main():
    clone_repos()


if __name__ == "__main__":
    main()
