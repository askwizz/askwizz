# syntax=docker/dockerfile:1

FROM python:3.11

ADD . /app/
WORKDIR /app/
# Now this is is the worst.
# - No caching of dependencies, we download and rebuild everything on every change in the code
# - No lockfile, pip does not look at poetry.lock
# Ideally we should install in steps like so
# ```
# ADD ./pyproject.toml ./poetry.lock /app/
# poetry install --only main --no-root
# ADD . /app/
# poetry install --root-only
# ```
# but that leads to libcublas and such not to be found.
# 
# Hey, at least this works. U_U
RUN python -m pip install .
