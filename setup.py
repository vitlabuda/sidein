#!/bin/false

# Copyright (c) 2022 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import sys
import os
import os.path
__REPOSITORY_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
if __REPOSITORY_ROOT_DIR not in sys.path:
    sys.path.insert(0, __REPOSITORY_ROOT_DIR)
os.chdir(__REPOSITORY_ROOT_DIR)

import setuptools
from sidein.SideinConstants import SideinConstants


with open("./README.md", "r") as readme_io:
    readme_text = readme_io.read()


setuptools.setup(
    name="sidein",
    version=SideinConstants.LIBRARY_VERSION,
    description="A flexible, object-oriented Python dependency injector",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="Vít Labuda",
    author_email="dev@vitlabuda.cz",
    license="BSD License",
    url="https://github.com/vitlabuda/sidein",
    project_urls={
        "Bug Tracker": "https://github.com/vitlabuda/sidein/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    tests_require=["pytest"],
)
