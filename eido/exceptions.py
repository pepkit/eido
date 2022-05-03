""" Exceptions for specific eido issues. """

from abc import ABCMeta

_all__ = ["PathAttrNotFoundError", "EidoSchemaInvalidError", "EidoFilterError"]


class EidoException(Exception):
    """Base type for custom package errors."""

    __metaclass__ = ABCMeta


class PathAttrNotFoundError(EidoException):
    """Path-like argument does not exist."""

    def __init__(self, key):
        super(PathAttrNotFoundError, self).__init__(key)


class EidoSchemaInvalidError(EidoException):
    """Schema does not comply to eido-specific requirements."""

    def __init__(self, key):
        super(EidoSchemaInvalidError, self).__init__(key)


class EidoFilterError(EidoException):
    """Issue with the PEP filter."""

    def __init__(self, key):
        super(EidoFilterError, self).__init__(key)
