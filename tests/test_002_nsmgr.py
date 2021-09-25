# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2021 Vít Labuda. All rights reserved.
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


import pytest
from sidein.Sidein import Sidein
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.nsmgr.exc.NamespaceExistsException import NamespaceExistsException
from sidein.nsmgr.exc.NamespaceNotFoundException import NamespaceNotFoundException


namespace_names = ("", "com.example.namespace", "namespace with spaces", "🤍🤎")


@pytest.fixture
def nsmgr():
    nsmgr = Sidein.get_namespace_manager()
    yield nsmgr
    nsmgr.remove_all_namespaces()


@pytest.mark.parametrize("ns_name", namespace_names)
def test_automatic_ns_creation(nsmgr, ns_name):
    ns = nsmgr.add_namespace_if_not_exists_and_get_it(ns_name)
    assert isinstance(ns, NamespaceInterface)


@pytest.mark.parametrize("ns_name", namespace_names)
def test_non_existing_ns_acquisition(nsmgr, ns_name):
    with pytest.raises(NamespaceNotFoundException):
        nsmgr.get_namespace(ns_name)


def test_all_ns_acquisition(nsmgr):
    for ns_name in namespace_names:
        nsmgr.add_namespace(ns_name)

    all_ns = nsmgr.get_all_namespaces()
    assert isinstance(all_ns, dict)
    assert len(all_ns) == len(namespace_names)


@pytest.mark.parametrize("ns_name", namespace_names)
def test_ns_addition(nsmgr, ns_name):
    nsmgr.add_namespace(ns_name)
    ns = nsmgr.get_namespace(ns_name)
    assert isinstance(ns, NamespaceInterface)


@pytest.mark.parametrize("ns_name", namespace_names)
def test_already_existing_ns_addition(nsmgr, ns_name):
    nsmgr.add_namespace(ns_name)
    with pytest.raises(NamespaceExistsException):
        nsmgr.add_namespace(ns_name)


@pytest.mark.parametrize("ns_name", namespace_names)
def test_ns_removal(nsmgr, ns_name):
    nsmgr.add_namespace(ns_name)
    nsmgr.remove_namespace(ns_name)
    with pytest.raises(NamespaceNotFoundException):
        nsmgr.get_namespace(ns_name)


@pytest.mark.parametrize("ns_name", namespace_names)
def test_non_existing_ns_removal(nsmgr, ns_name):
    with pytest.raises(NamespaceNotFoundException):
        nsmgr.remove_namespace(ns_name)


def test_all_ns_removal(nsmgr):
    for ns_name in namespace_names:
        nsmgr.add_namespace(ns_name)

    assert len(nsmgr.get_all_namespaces()) == len(namespace_names)

    nsmgr.remove_all_namespaces()
    assert len(nsmgr.get_all_namespaces()) == 0
