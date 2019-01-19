#!/usr/bin/env python
#
#  Sync repositories with local .debs. Will not re-push if files already exist.
#
import getpass
import os
import requests

BASE_URL = "https://repositories.ecg.so/v1"
# Hardcoded for now. Excercise for reader
DISTRIBUTION = "trusty"
SECTION = "main"

REPO_URL = os.path.join(BASE_URL, DISTRIBUTION, SECTION)


def get_current_packages(repo_pass):
    """Returns the current packages in the repository as a list of (name,version) tuples"""
    response = requests.get(REPO_URL, auth=(USER, repo_pass)).json()
    result = [tuple(elem.split('=')) for elem in response['result']]
    return result


def get_local_debs():
    """Returns the debian packages in the local directory as a list of (name, version, deb) tuples"""
    def filename_to_tuple(f):
        parts = f.split('_')
        return parts[0], parts[1], f
    return [filename_to_tuple(elem) for elem in os.listdir(".") if elem.endswith(".deb")]


def upload_debian(deb, repo_user, repo_pass):
    length = os.path.getsize(deb)
    print "========== Uploading debian package", deb, "(%d bytes)" % length
    with open(deb, 'rb') as dh:
        response = requests.put(REPO_URL, auth=(repo_user, repo_pass),
                                files={'filedata': dh})
        return response.json()


def run():
    def key_from_tuple(t):
        return "%s-%s" % (t[0], t[1])
    repo_user = get_repo_user()
    repo_pass = get_repo_pass()
    packages = get_current_packages(repo_pass)
    local_debs = get_local_debs()
    package_dict = {key_from_tuple(p): True for p in packages}
    missing = [d for d in local_debs if not key_from_tuple(d) in package_dict]
    if not missing:
        print "All ok, nothing to do"
    else:
        for deb in missing:
            print upload_debian(deb[2], repo_user, repo_pass)


def get_repo_user():
    return raw_input("Enter repo user name: ")


def get_repo_pass():
    return getpass.getpass('Enter repo password: ')


if __name__ == '__main__':
    run()