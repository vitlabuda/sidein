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

from typing import List
import pytest
import threading
from sidein.Sidein import Sidein
from sidein.providers.simplecontainer.ThreadLocalSimpleContainer import ThreadLocalSimpleContainer


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


@pytest.fixture
def container():
    ns_name = __file__

    ns_ = Sidein.ns(ns_name)
    ns_.set_dependency_provider(ThreadLocalSimpleContainer())
    yield ns_.get_dependency_provider()

    Sidein.get_namespace_manager().remove_namespace(ns_name)


# As of now, the implementation of thread-local simple container differs from the global simple container only in the
# dependency storage (thread-local vs. global). As global simple container is tested too, the only thing that's tested
# here is that the thread-local storage is really thread-local.


def test_dependency_storage_thread_locality(container):
    def _count_dependencies(save_count_here: List[int]) -> None:
        save_count_here.append(len(container.get_all_dependencies()))

    for dep_name in dependency_names:
        container.add_dependency(dep_name, make_dummy_dep(dep_name))

    main_dep_count, thread_dep_count = [], []

    _count_dependencies(main_dep_count)
    t = threading.Thread(target=_count_dependencies, args=(thread_dep_count,))
    t.start()
    t.join()

    assert isinstance(main_dep_count[0], int)
    assert isinstance(thread_dep_count[0], int)
    assert main_dep_count[0] == len(dependency_names)
    assert thread_dep_count[0] == 0
