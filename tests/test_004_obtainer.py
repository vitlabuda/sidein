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


from typing import Any
import pytest
from sidein.Sidein import Sidein
from sidein.providers.DependencyProviderInterface import DependencyProviderInterface
from sidein.providers.exc.DependencyProviderException import DependencyProviderException
from sidein.obtainer.DependencyObtainerInterface import DependencyObtainerInterface


dependency_names = ("", "com.example.dependency", "dependency with spaces", "⬛️⬜️")
failing_dependency_names = ("fail 1", "fail 2", "fail 3")


class DummyDependencyProvider(DependencyProviderInterface):
    def __init__(self):
        self._dependency: Any = "initial dependency"

    def get_dependency(self, name: str) -> Any:
        if name in failing_dependency_names:
            raise DependencyProviderException("Dependency provider failure requested.")

        return self._dependency

    def set_dependency(self, value: Any) -> None:
        self._dependency = value


@pytest.fixture
def ns():
    ns_name = __file__

    ns_ = Sidein.ns(ns_name)
    ns_.set_dependency_provider(DummyDependencyProvider())
    yield ns_

    Sidein.get_namespace_manager().remove_namespace(ns_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_obtainer_acquisition(ns, dep_name):
    obtainer = ns.get_dependency(dep_name, in_obtainer=True)
    assert isinstance(obtainer, DependencyObtainerInterface)


def test_multiple_obtainers_acquisition(ns):
    obtainers = ns.get_dependencies(*dependency_names, in_obtainers=True)

    assert isinstance(obtainers, dict)
    assert len(obtainers) == len(dependency_names)

    for obtainer in obtainers.values():
        assert isinstance(obtainer, DependencyObtainerInterface)


@pytest.mark.parametrize("failing_dep_name", failing_dependency_names)
def test_failing_obtainer_acquisition(ns, failing_dep_name):
    with pytest.raises(DependencyProviderException):
        ns.get_dependency(failing_dep_name, in_obtainer=True).obtain_dependency()


def test_multiple_failing_obtainers_acquisition(ns):
    with pytest.raises(DependencyProviderException):
        for obtainer in ns.get_dependencies(*failing_dependency_names, in_obtainers=True).values():
            obtainer.obtain_dependency()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_name_acquisition_from_obtainer(ns, dep_name):
    obtainer = ns.get_dependency(dep_name, in_obtainer=True)

    assert obtainer.get_dependency_name() == dep_name


@pytest.mark.parametrize("dep_name", dependency_names)
def test_obtainer_injection(ns, dep_name):
    @ns.inject_dependencies(dep_name, in_obtainers=True, as_kwargs=True)
    def _inject_here(*args, **kwargs):
        assert len(args) == 0
        assert len(kwargs) == 1
        assert isinstance(kwargs[dep_name], DependencyObtainerInterface)

    _inject_here()


@pytest.mark.parametrize("failing_dep_name", failing_dependency_names)
def test_failing_obtainer_injection(ns, failing_dep_name):
    @ns.inject_dependencies(failing_dep_name, in_obtainers=True, as_kwargs=True)
    def _inject_here(*args, **kwargs):
        assert len(args) == 0
        assert len(kwargs) == 1

        obtainer = kwargs[failing_dep_name]
        with pytest.raises(DependencyProviderException):
            obtainer.obtain_dependency()

    _inject_here()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_bound_dependency_modification_with_acquisition(ns, dep_name):
    old_dependency = ns.get_dependency(dep_name)
    new_dependency = __file__ + test_bound_dependency_modification_with_acquisition.__qualname__

    obtainer = ns.get_dependency(dep_name, in_obtainer=True)
    assert obtainer.get_dependency_name() == dep_name

    assert obtainer.obtain_dependency() == old_dependency
    ns.get_dependency_provider().set_dependency(new_dependency)
    assert obtainer.obtain_dependency() == new_dependency


@pytest.mark.parametrize("dep_name", dependency_names)
def test_bound_dependency_modification_with_injection(ns, dep_name):
    @ns.inject_dependencies(dep_name, in_obtainers=True, as_kwargs=True)
    def _inject_here(*args, **kwargs):
        assert len(args) == 0
        assert len(kwargs) == 1

        old_dependency = ns.get_dependency(dep_name)
        new_dependency = __file__ + test_bound_dependency_modification_with_injection.__qualname__

        obtainer = kwargs[dep_name]
        assert obtainer.get_dependency_name() == dep_name

        assert obtainer.obtain_dependency() == old_dependency
        ns.get_dependency_provider().set_dependency(new_dependency)
        assert obtainer.obtain_dependency() == new_dependency

    _inject_here()
