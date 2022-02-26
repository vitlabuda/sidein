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

from typing import Any
import pytest
import asyncio
from sidein.Sidein import Sidein
from sidein.providers.DependencyProviderInterface import DependencyProviderInterface
from sidein.providers.exc.DependencyProviderException import DependencyProviderException
from sidein.providers.simplecontainer.GlobalSimpleContainer import GlobalSimpleContainer
from sidein.ns.exc.NotAFunctionError import NotAFunctionError
from sidein.ns.exc.DependencyProviderRaisedAnExceptionError import DependencyProviderRaisedAnExceptionError
from sidein.ns.exc.DuplicateDependencyRequestedError import DuplicateDependencyRequestedError
from sidein.ns.exc.decoration.InvalidDecoratorError import InvalidDecoratorError
from sidein.ns.exc.decoration.InvalidDecoratorExtractorError import InvalidDecoratorExtractorError


dependency_names = (
    "",
    "   ",
    "\r\n",
    "com.example.dependency",
    "dependency with spaces",
    "řeřicha",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy. ",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.\n",
    "🤍🤎",
    "⬛️⬜️",
)
failing_dependency_names = ("fail 1", "fail 2", "fail 3")
unexpectedly_failing_dependency_names = ("unexpected fail 1", "unexpected fail 2")
decorator_dependency_names = ("decorator 1", "decorator 2")
parametrized_decorator_dependency_names = ("parametrized decorator 1", "parametrized decorator 2")


class DummyDependencyProvider(DependencyProviderInterface):
    def get_dependency(self, name: str) -> Any:
        if name in failing_dependency_names:
            raise DependencyProviderException("Dependency provider failure requested.")

        if name in unexpectedly_failing_dependency_names:
            raise ValueError("Unexpected failure requested.")

        if name in decorator_dependency_names:
            return lambda func: (lambda *args, **kwargs: name)

        if name in parametrized_decorator_dependency_names:
            return lambda ret_val: (lambda func: (lambda *args, **kwargs: ret_val))

        return name


@pytest.fixture
def ns():
    ns_name = __file__

    ns_ = Sidein.ns(ns_name)
    ns_.set_dependency_provider(DummyDependencyProvider())
    yield ns_

    Sidein.get_namespace_manager().remove_namespace(ns_name)


def test_dependency_provider_acquision(ns):
    dp = ns.get_dependency_provider()
    assert isinstance(dp, DependencyProviderInterface)


def test_dependency_provider_alteration(ns):
    dummy_dp = DummyDependencyProvider()

    ns.set_dependency_provider(dummy_dp)
    assert ns.get_dependency_provider() is dummy_dp


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_acquisition(ns, dep_name):
    dep = ns.get_dependency(dep_name)
    assert dep == dep_name


@pytest.mark.parametrize("failing_dep_name", failing_dependency_names)
def test_failing_dependency_acquisition(ns, failing_dep_name):
    with pytest.raises(DependencyProviderException):
        ns.get_dependency(failing_dep_name)


@pytest.mark.parametrize("unexpectedly_failing_dep_name", unexpectedly_failing_dependency_names)
def test_unexpectedly_failing_dependency_acquisition(ns, unexpectedly_failing_dep_name):
    with pytest.raises(DependencyProviderRaisedAnExceptionError):
        ns.get_dependency(unexpectedly_failing_dep_name)


def test_multiple_dependencies_acquisition(ns):
    deps = ns.get_dependencies(*dependency_names)
    assert isinstance(deps, dict)
    assert len(deps) == len(dependency_names)


def test_multiple_failing_dependencies_acquisition(ns):
    with pytest.raises(DependencyProviderException):
        ns.get_dependencies(*failing_dependency_names)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_duplicate_dependencies_acquisition(ns, dep_name):
    with pytest.raises(DuplicateDependencyRequestedError):
        ns.get_dependencies(dep_name, dep_name)


@pytest.mark.parametrize("dep_name", dependency_names)
def test_kwargs_dependency_injection(ns, dep_name):
    @ns.inject_dependencies(dep_name, as_kwargs=True)
    def _inject_here(*args, **kwargs):
        assert len(args) == 0
        assert len(kwargs) == 1
        assert kwargs[dep_name] == dep_name

    _inject_here()


def test_kwargs_dependency_injection_with_multiple_dependencies(ns):
    @ns.inject_dependencies(*dependency_names, as_kwargs=True)
    def _inject_here(*args, **kwargs):
        assert len(args) == 0
        assert len(kwargs) == len(dependency_names)
        for key, value in kwargs.items():
            assert key == value

    _inject_here()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_kwargs_duplicate_dependency_injection(ns, dep_name):
    @ns.inject_dependencies(dep_name, dep_name, as_kwargs=True)
    def _inject_here():
        pytest.fail("Injecting duplicate dependencies shouldn't be possible and this statement should've never got executed!")

    with pytest.raises(DuplicateDependencyRequestedError):
        _inject_here()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_args_dependency_injection(ns, dep_name):
    @ns.inject_dependencies(dep_name, as_kwargs=False)
    def _inject_here(*args, **kwargs):
        assert len(args) == 1
        assert len(kwargs) == 0
        assert args[0] == dep_name

    _inject_here()


def test_args_dependency_injection_multiple_dependencies(ns):
    @ns.inject_dependencies(*dependency_names, as_kwargs=False)
    def _inject_here(*args, **kwargs):
        assert len(args) == len(dependency_names)
        assert len(kwargs) == 0
        for i in range(len(dependency_names)):
            assert dependency_names[i] == args[i]  # Checks whether the order was preserved

    _inject_here()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_args_duplicate_dependency_injection(ns, dep_name):
    @ns.inject_dependencies(dep_name, dep_name, as_kwargs=False)
    def _inject_here():
        pytest.fail("Injecting duplicate dependencies shouldn't be possible and this statement should've never got executed!")

    with pytest.raises(DuplicateDependencyRequestedError):
        _inject_here()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_kwargs_dependency_injection_to_async_function(ns, dep_name):
    @ns.inject_dependencies(dep_name)
    async def _inject_here_async(*args, **kwargs):
        assert len(args) == 0
        assert len(kwargs) == 1
        assert kwargs[dep_name] == dep_name

    asyncio.run(_inject_here_async())


@pytest.mark.parametrize("dep_name", dependency_names)
def test_class_dependency_injection(ns, dep_name):
    with pytest.raises(NotAFunctionError):
        @ns.inject_dependencies(dep_name)
        class _InjectHere:
            pass


@pytest.mark.parametrize("failing_dep_name", failing_dependency_names)
def test_failing_dependency_injection(ns, failing_dep_name):
    @ns.inject_dependencies(failing_dep_name)
    def _inject_here():
        pytest.fail("The dependency injection was supposed to fail and this statement should've never got executed!")

    with pytest.raises(DependencyProviderException):
        _inject_here()


@pytest.mark.parametrize("unexpectedly_failing_dep_name", unexpectedly_failing_dependency_names)
def test_unexpectedly_failing_dependency_injection(ns, unexpectedly_failing_dep_name):
    @ns.inject_dependencies(unexpectedly_failing_dep_name)
    def _inject_here():
        pytest.fail("The dependency injection was supposed to fail and this statement should've never got executed!")

    with pytest.raises(DependencyProviderRaisedAnExceptionError):
        _inject_here()


@pytest.mark.parametrize("decorator_dep_name", decorator_dependency_names)
def test_dependency_decoration(ns, decorator_dep_name):
    @ns.decorate_with_dependency(decorator_dep_name)
    def _decorate_this():
        pytest.fail("The dummy decorator should not call the decorated method!")

    assert _decorate_this() == decorator_dep_name


@pytest.mark.parametrize("parametrized_decorator_dep_name", parametrized_decorator_dependency_names)
def test_dependency_decoration_with_parametrized_decorator(ns, parametrized_decorator_dep_name):
    return_value = parametrized_decorator_dep_name + " return value"

    @ns.decorate_with_dependency(parametrized_decorator_dep_name, lambda dependency: dependency(return_value))
    def _decorate_this():
        pytest.fail("The dummy decorator should not call the decorated method!")

    assert _decorate_this() == return_value


@pytest.mark.parametrize("decorator_dep_name", decorator_dependency_names)
def test_class_dependency_decoration(ns, decorator_dep_name):
    with pytest.raises(NotAFunctionError):
        @ns.decorate_with_dependency(decorator_dep_name)
        class _DecorateThis:
            pass


@pytest.mark.parametrize("failing_dep_name", failing_dependency_names)
def test_failing_dependency_decoration(ns, failing_dep_name):
    @ns.decorate_with_dependency(failing_dep_name)
    def _decorate_this():
        pytest.fail("The decoration was supposed to fail and this statement should've never got executed!")

    with pytest.raises(DependencyProviderException):
        _decorate_this()


@pytest.mark.parametrize("dep_name", dependency_names)
def test_dependency_decoration_with_invalid_decorator(ns, dep_name):
    @ns.decorate_with_dependency(dep_name)
    def _decorate_this():
        pytest.fail("The decoration was supposed to fail and this statement should've never got executed!")

    with pytest.raises(InvalidDecoratorError):
        _decorate_this()


@pytest.mark.parametrize("parametrized_decorator_dep_name", parametrized_decorator_dependency_names)
def test_dependency_decoration_with_invalid_extractor(ns, parametrized_decorator_dep_name):
    @ns.decorate_with_dependency(parametrized_decorator_dep_name, "invalid extractor")
    def _decorate_this():
        pytest.fail("The decoration was supposed to fail and this statement should've never got executed!")

    with pytest.raises(InvalidDecoratorExtractorError):
        _decorate_this()


def test_default_dependency_provider_implementation():
    ns_name = __file__ + test_default_dependency_provider_implementation.__qualname__

    ns_ = Sidein.ns(ns_name)
    try:
        provider = ns_.get_dependency_provider()
        assert isinstance(provider, GlobalSimpleContainer)

    finally:
        Sidein.get_namespace_manager().remove_namespace(ns_name)
