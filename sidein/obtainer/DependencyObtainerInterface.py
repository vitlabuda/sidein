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


from typing import Any
import abc


class DependencyObtainerInterface(metaclass=abc.ABCMeta):
    """
    Dependency obtainer objects are responsible for holding a dependency's name and the namespace from which the
     dependency comes from.

    This enables dependants to acquire the dependency later and/or repeatedly which is useful e.g. when the dependant
     needs to replace the dependency provider and needs to get an updated reference to the dependency after that.

    The purpose of this class might be quite tricky to understand just from the above explanation - I recommend you to
     take a look at the examples if you want to make use of this feature.
    """

    __slots__ = ()

    @abc.abstractmethod
    def get_dependency_name(self) -> str:
        """
        Returns the name of the dependency bound to the dependency obtainer.

        :return: The name of the dependency bound to the dependency obtainer.
        """

        raise NotImplementedError(DependencyObtainerInterface.get_dependency_name.__qualname__)

    @abc.abstractmethod
    def obtain_dependency(self) -> Any:
        """
        Obtains the dependency bound to the dependency obtainer from the bound namespace and returns it.

        :return: The dependency bound to the dependency obtainer.
        :raises DependencyProviderException: If anything goes wrong in the dependency provider (e.g. if the dependency couldn't be found).
        """

        raise NotImplementedError(DependencyObtainerInterface.obtain_dependency.__qualname__)
