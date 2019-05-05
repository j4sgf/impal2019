import sys
import os
import io
import contextlib
from setuptools import setup, find_packages


@contextlib.contextmanager
def chdir(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        sys.path.insert(0, new_dir)
        yield
    finally:
        del sys.path[0]
        os.chdir(old_dir)


def setup_pack():

    base_dir = os.path.abspath(os.path.dirname(__file__))

    with chdir(base_dir):
        with io.open(os.path.join(base_dir, 'qna', 'about.py')) as fp:
            about = {}
            exec(fp.read(), about)

    with io.open(os.path.join(base_dir, 'readme.rst')) as f:
        readme = f.read()

    setup(name=about['__title__'], packages=find_packages(
    ), description=about['__summary__'], long_description=readme, version=about['__version__'])


if __name__ == "__main__":
    setup_pack()
