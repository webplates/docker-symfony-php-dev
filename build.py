from dockermatrix import *
import getpass
import itertools
import os

DIST = "images"
BRANCH = "images"
REPO = "webplates/symfony-php-dev"

VERSIONS = ["5.6.26", "7.0.11"]
VARIANTS = ["fpm"]

MATRIX = set(itertools.chain(
    itertools.product(VERSIONS, [None], [None]),
    itertools.product(VERSIONS, VARIANTS, [None])
))

build_matrix = create_build_matrix(MATRIX)
dockerfile_builder = DockerfileBuilder()
hub_updater = HubUpdater(os.environ.get("DOCKERHUB_USERNAME"), os.environ.get("DOCKERHUB_PASSWORD", getpass.getpass("Enter Docker Hub password: ")))

images = build_matrix.build(DIST)

dockerfile_builder.build(images, DIST)

hub_updater.login()
hub_updater.clear_builds(REPO)
hub_updater.add_builds(REPO, BRANCH, images)
