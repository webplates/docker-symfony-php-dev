from dockermatrix import *
import argparse
import getpass
import itertools
import os
import sys

DIST = "images"
BRANCH = "images"
REPO = "webplates/symfony-php-dev"

VERSIONS = ["5.6.26", "7.0.11"]
VARIANTS = ["fpm"]

MATRIX = set(itertools.chain(
    itertools.product(VERSIONS, [None], [None]),
    itertools.product(VERSIONS, VARIANTS, [None])
))

parser = argparse.ArgumentParser(description="Build option parse.")
parser.add_argument("--dockerhub", action="store_true", default=False, help="Notify Docker Hub about rebuilt images")

args = parser.parse_args()

build_matrix = create_build_matrix(MATRIX)
dockerfile_builder = DockerfileBuilder()

if args.dockerhub:
    if "DOCKERHUB_USERNAME" not in os.environ or not os.environ["DOCKERHUB_USERNAME"]:
        username = input("Enter Docker Hub username: ")
    else:
        username = os.environ["DOCKERHUB_USERNAME"]

    if "DOCKERHUB_PASSWORD" not in os.environ or not os.environ["DOCKERHUB_PASSWORD"]:
        password = getpass.getpass("Enter Docker Hub password: ")
    else:
        password = os.environ["DOCKERHUB_PASSWORD"]

    hub_updater = HubUpdater(username, password)

    try:
        hub_updater.login()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


images = build_matrix.build(DIST)

dockerfile_builder.build(images, DIST)

if args.dockerhub:
    hub_updater.clear_builds(REPO)
    hub_updater.add_builds(REPO, BRANCH, images)
