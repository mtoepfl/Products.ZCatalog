##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from Acquisition import Implicit
from Acquisition import ImplicitAcquisitionWrapper
from Acquisition import aq_base
from Acquisition import aq_get
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.globalrequest import getRequest
from zope.interface import implementer
from ZPublisher.BaseRequest import RequestContainer

from .interfaces import ICatalogBrain


EXCEPTION_MSG_NOT_MUTEABE = "LazyBrain is not muteable"


"""

No inheritance because of performance reasons, base-classes did not change within many years. Thats why the code was repeatet.

TODO: Document it in AbstractCatalogBrain (or Record) that fixes has to be done in LazyBrain too

"""



@implementer(ICatalogBrain)
class LazyBrain:
    """Performance optimized brain for ZCatalog"""

    #__allow_access_to_unprotected_subobjects__ = 1
    #__record_schema__ = None
    __slots__ = ('__data__', '__record_schema__', 'data_record_id_', '__context__', 'data_record_score_', 'data_record_normalized_score_')
    __LEN__ = None


    # Record

    def __new__(cls, data=None, parent=None):
        obj = super().__new__(cls)
        obj.__setstate__(data)
        return obj

    def __getstate__(self):
        return self.__data__

    def __setstate__(self, data):
        self.__data__ = data # no copy any longer

    def __getitem__(self, key):
        if isinstance(key, int):
            pos = key
        else:
            pos = getattr(self.__record_schema__, key)
        return self.__data__[pos]

    def __getattr__(self, key):
        if key in self.__slots__:
            return object.__getattribute__(self, key)
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __setitem__(self, key, value):
        raise Exception(EXCEPTION_MSG_NOT_MUTEABE)

    def __setattr__(self, key, value):
        if key in self.__slots__:
            object.__setattr__(self, key, value)
        else:
            raise Exception(EXCEPTION_MSG_NOT_MUTEABE)

    def __delattr__(self, key):
        self[key] = None

    def __delitem__(self, key):
        raise Exception(EXCEPTION_MSG_NOT_MUTEABE)

    def __contains__(self, key):
        return key in self.__record_schema__

    def __getslice__(self, i, j):
        raise TypeError('Record objects do not support slicing')

    def __setslice__(self, i, j, sequence):
        raise TypeError('Record objects do not support slicing')

    def __delslice__(self, i, j):
        raise TypeError('Record objects do not support slicing')

    def __add__(self, other):
        raise TypeError('Record objects do not support concatenation')

    def __mul__(self, other):
        raise TypeError('Record objects do not support repetition')

    def __len__(self):
        return self.__record_schema__.__LEN__

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        if isinstance(other, Record):
            return self.__data__ < other.__data__
        return id(self) < id(other)

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__data__ == other.__data__
        return id(self) == id(other)

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)


    # AbstractCatalogBrain


    def has_key(self, key):
        return key in self.__record_schema__

    def __contains__(self, name):
        return name in self.__record_schema__

    def getPath(self):
        """Get the physical path for this record"""
        return aq_parent(aq_inner(self)).getpath(self.data_record_id_)

    def getURL(self, relative=0):
        """Generate a URL for this record"""
        request = aq_get(self, 'REQUEST', None)
        if request is None:
            request = getRequest()
        return request.physicalPathToURL(self.getPath(), relative)

    def _unrestrictedGetObject(self):
        """Return the object for this record

        Same as getObject, but does not do security checks.
        """
        parent = aq_parent(self)
        if (aq_get(parent, 'REQUEST', None) is None):
            request = getRequest()
            if request is not None:
                # path should be absolute, starting at the physical root
                parent = self.getPhysicalRoot()
                request_container = RequestContainer(REQUEST=request)
                parent = aq_base(parent).__of__(request_container)
        return parent.unrestrictedTraverse(self.getPath())

    def getObject(self, REQUEST=None):
        """Return the object for this record

        Will return None if the object cannot be found via its cataloged path
        (i.e., it was deleted or moved without recataloging), or if the user is
        not authorized to access the object.

        This method mimicks a subset of what publisher's traversal does,
        so it allows access if the final object can be accessed even
        if intermediate objects cannot.
        """
        path = self.getPath().split('/')
        if not path:
            return None
        parent = aq_parent(self)
        if (aq_get(parent, 'REQUEST', None) is None):
            request = getRequest()
            if request is not None:
                # path should be absolute, starting at the physical root
                parent = self.getPhysicalRoot()
                request_container = RequestContainer(REQUEST=request)
                parent = aq_base(parent).__of__(request_container)
        if len(path) > 1:
            parent = parent.unrestrictedTraverse(path[:-1])

        return parent.restrictedTraverse(path[-1])

    def getRID(self):
        """Return the record ID for this object."""
        return self.data_record_id_

    # Implicit

    def __of__(self, context):
        self.__context__ = context
        return ImplicitAcquisitionWrapper(self, context)

