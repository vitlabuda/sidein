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
if "SIDEIN_TESTS_AUTOPATH" in os.environ:
    __TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    __MODULE_DIR = os.path.realpath(os.path.join(__TESTS_DIR, ".."))
    if __TESTS_DIR not in sys.path:
        sys.path.insert(0, __TESTS_DIR)
    if __MODULE_DIR not in sys.path:
        sys.path.insert(0, __MODULE_DIR)

import pytest
from sidein.Sidein import Sidein
from sidein.providers.simplecontainer.GlobalSimpleContainer import GlobalSimpleContainer
from sidein.providers.exc.DependencyProviderException import DependencyProviderException
from sidein.providers.simplecontainer.exc.DependencyInSCNotFoundException import DependencyInSCNotFoundException
from sidein.providers.simplecontainer.exc.DependencyInSCExistsException import DependencyInSCExistsException


dependency_names = (
    "",
    "   ",
    "\r\n",
    "com.example.container_dependency",
    "container dependency with spaces",
    "řeřicha",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy. ",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.\n",
    "🤍🤎",
    "🕐🕑🕒🕓",
)


def make_dummy_dep(dep_name: str) -> str:
    return dep_name + " dependency value"


def make_new_dummy_dep(dep_name: str) -> str:
    return make_dummy_dep(dep_name) + " NEW"


@pytest.fixture
def container():
    ns_name = __file__

    ns_ = Sidein.ns(ns_name)
    ns_.set_dependency_provider(GlobalSimpleContainer())
    yield ns_.get_dependency_provider()

    Sidein.get_namespace_manager().remove_namespace(ns_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_non_existing_dependency_acquisition(container, dep_name):
    with pytest.raises(DependencyProviderException):
        container.get_dependency(dep_name)


def test_all_dependencies_acquisition(container):
    for dep_name in dependency_names:
        container.add_dependency(dep_name, make_dummy_dep(dep_name))

    all_deps = container.get_all_dependencies()
    assert isinstance(all_deps, dict)
    assert len(all_deps) == len(dependency_names)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_addition(container, dep_name):
    container.add_dependency(dep_name, make_dummy_dep(dep_name))

    assert container.get_dependency(dep_name) == make_dummy_dep(dep_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_already_existing_dependency_addition(container, dep_name):
    container.add_dependency(dep_name, make_dummy_dep(dep_name))

    with pytest.raises(DependencyInSCExistsException):
        container.add_dependency(dep_name, make_dummy_dep(dep_name))


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_replacement(container, dep_name):
    container.add_dependency(dep_name, make_dummy_dep(dep_name))

    container.replace_dependency(dep_name, make_new_dummy_dep(dep_name))
    assert container.get_dependency(dep_name) == make_new_dummy_dep(dep_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_non_existing_dependency_replacement(container, dep_name):
    with pytest.raises(DependencyInSCNotFoundException):
        container.replace_dependency(dep_name, make_dummy_dep(dep_name))


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_addition_or_replacement(container, dep_name):
    container.add_or_replace_dependency(dep_name, make_dummy_dep(dep_name))

    container.add_or_replace_dependency(dep_name, make_new_dummy_dep(dep_name))
    assert container.get_dependency(dep_name) == make_new_dummy_dep(dep_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_removal(container, dep_name):
    container.add_dependency(dep_name, make_dummy_dep(dep_name))

    container.remove_dependency(dep_name)
    with pytest.raises(DependencyInSCNotFoundException):
        container.get_dependency(dep_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_non_existing_dependency_removal(container, dep_name):
    with pytest.raises(DependencyInSCNotFoundException):
        container.remove_dependency(dep_name)


def test_all_dependencies_removal(container):
    for dep_name in dependency_names:
        container.add_dependency(dep_name, make_dummy_dep(dep_name))

    assert len(container.get_all_dependencies()) == len(dependency_names)

    container.remove_all_dependencies()
    assert len(container.get_all_dependencies()) == 0
