"""Defines the base class for simple types."""

# --------------------------------------------------------------------------
# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2009, Python File Format Interface
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the Python File Format Interface
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****
# --------------------------------------------------------------------------

import PyFFI.ObjectModels.AnyType

class SimpleType(PyFFI.ObjectModels.AnyType.AnyType):
    """Base class from which all simple types are derived. Simple
    types contain data which is not divided further into smaller pieces,
    and that can represented efficiently by a (usually native) Python type,
    typically C{int}, C{float}, or L{str}.

    A brief example of usage (without type checking):

    >>> class Int(SimpleType):
    ...     def __init__(self, value=None):
    ...         self.value = 0 if value is None else value
    >>> print(Int(value=12345))
    12345

    A slightly more complicated example, demonstrating how to implement
    type checking:

    >>> class Short(SimpleType):
    ...     def __init__(self, value=None):
    ...         # for fun, let default value be 3
    ...         self.value = 3 if value is None else value
    ...     def _get(self):
    ...         return self._value
    ...     def _set(self, value):
    ...         # check type
    ...         if not isinstance(value, int):
    ...             raise TypeError("Expected int but got %s."
    ...                             % value.__class__.__name__)
    ...         # check range
    ...         if value < -0x8000 or value > 0x7fff:
    ...             raise ValueError("Value %i out of range." % value)
    ...         self._value = value
    ...     value = property(_get, _set)
    >>> print(Short(value=15))
    15
    >>> test = Short()
    >>> print(test)
    3
    >>> test.value = 255
    >>> print(test)
    255
    >>> test.value = 100000 # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> test.value = "hello world" # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...

    Also override L{read} and L{write} if you wish to read and write data
    of this type, and L{isInterchangeable} if you wish to declare data as
    equivalent.

    @ivar value: The actual data.
    @type value: C{type(None)}, or anything of the appropriate type.
    """

    def __init__(self, value=None):
        """Initialize the type with given value.

        @keyword value: The initial value of the object.
        @type value: C{type(None)}, or anything of the appropriate type.
        """
        self.value = value

    def __str__(self):
        """String representation. This implementation is simply a wrapper
        around C{self.L{value}.__str__()}.

        @return: String representation.
        @rtype: C{str}
        """
        return self.value.__str__()

    # AnyType

    def isInterchangeable(self, other):
        """This checks for object identity of the value."""
        return self.value is other.value

    # DetailNode

    def getDetailDisplay(self):
        """Display string for the detail tree. This implementation is simply
        a wrapper around C{self.L{value}.__str__()}.

        @return: String representation.
        @rtype: C{str}
        """
        return self.value.__str__()

