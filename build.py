from dockermatrix import *
import itertools

DIST = "images"
BRANCH = "images"
REPO = "webplates/symfony-php-dev"

VERSIONS = ["5.6.26", "7.0.11"]
VARIANTS = ["fpm"]

MATRIX = set(itertools.product(VERSIONS, itertools.chain(
    itertools.product([None], [None]),
    itertools.product(VARIANTS, [None])
)))

build_matrix = create_build_matrix(MATRIX)
builder = Builder()

images = build_matrix.build(DIST)

builder.build(images, REPO, BRANCH, DIST)
