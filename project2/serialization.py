"""
Serialisation for Petrelic's binary types.

!!! DO NOT MODIFY THIS FILE !!!

For this project, data can be serialized with the library `jsonpickle`.
The underlying library, `pickle`, is notoriously insecure, and should never be
used to de-serialize untrusted data. Therefore, even if this serialization
library is OK for a student project of this scope, it should never be used for
a real life project.

One of the reason why `jsonpickle` is proposed is that is it easy to use, and
allows you to concentrate on the important parts of the project. Here is an
example:

>>> import jsonpickle
>>> class Foo:
...    def __init__(self):
...        self.a = 'Foo'
...        self.b = 42
...    def __eq__(self, other):
...        return self.a == other.a and self.b == other.b
...
>>> x_ori = Foo()
>>> x_ser = jsonpickle.encode(x_ori)
>>> x_des = jsonpickle.decode(x_ser)
>>> x_ori == x_des
True

Because the `petrelic` library binds some binary types, `jsonpickle` needs to
know how to handle them. Therefore, some handlers are defined and registered in
this file. As such, if you need to serialize an object containing some
`petrelic` types, with `jsonpickle`, you can do so by importing the "extended"
`jsonpickle` from this sub-module such as:

>>> from serialization import jsonpickle

"""

import base64

import jsonpickle

from petrelic.bn import Bn
from petrelic.additive.pairing import (
    G1Element as G1EA,
    G2Element as G2EA,
    GTElement as GtEA,
)
from petrelic.multiplicative.pairing import (
    G1Element as G1EM,
    G2Element as G2EM,
    GTElement as GtEM,
)
from petrelic.native.pairing import (
    G1Element as G1EN,
    G2Element as G2EN,
    GTElement as GtEN,
)
from petrelic.petlib.pairing import G1Elem as G1EP, G2Elem as G2EP, GTElem as GtEP

#
# Define handlers for jsonpickle.
#

# Handler for big number ised intrnally by RELIC.


class BnHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for Bn"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return Bn.from_binary(base64.b64decode(obj["b64repr"]))


# Handlers for additive API.


class G1EAHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G1Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G1EA.from_binary(base64.b64decode(obj["b64repr"]))


class G2EAHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G2Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G2EA.from_binary(base64.b64decode(obj["b64repr"]))


class GtEAHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for GtElement"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return GtEA.from_binary(base64.b64decode(obj["b64repr"]))


# Handlers for multiplicative API.


class G1EMHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G1Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G1EM.from_binary(base64.b64decode(obj["b64repr"]))


class G2EMHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G2Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G2EM.from_binary(base64.b64decode(obj["b64repr"]))


class GtEMHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for GtElement"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return GtEM.from_binary(base64.b64decode(obj["b64repr"]))


# Handlers for RELIC's native API.


class G1ENHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G1Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G1EN.from_binary(base64.b64decode(obj["b64repr"]))


class G2ENHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G2Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G2EN.from_binary(base64.b64decode(obj["b64repr"]))


class GtENHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for GtElement"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return GtEN.from_binary(base64.b64decode(obj["b64repr"]))


# Handlers for petlib's API.


class G1EPHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G1Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G1EP.from_binary(base64.b64decode(obj["b64repr"]))


class G2EPHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for G2Element"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return G2EP.from_binary(base64.b64decode(obj["b64repr"]))


class GtEPHandler(jsonpickle.handlers.BaseHandler):
    """JSONPickle handler for GtElement"""

    def flatten(self, obj, data):
        data["b64repr"] = base64.b64encode(obj.to_binary()).decode("utf-8")
        return data

    def restore(self, obj):
        return GtEP.from_binary(base64.b64decode(obj["b64repr"]))


# Register handlers for jsonpickle.

jsonpickle.handlers.register(Bn, BnHandler, base=True)

jsonpickle.handlers.register(G1EA, G1EAHandler, base=True)
jsonpickle.handlers.register(G2EA, G2EAHandler, base=True)
jsonpickle.handlers.register(GtEA, GtEAHandler, base=True)

jsonpickle.handlers.register(G1EM, G1EMHandler, base=True)
jsonpickle.handlers.register(G2EM, G2EMHandler, base=True)
jsonpickle.handlers.register(GtEM, GtEMHandler, base=True)

jsonpickle.handlers.register(G1EN, G1ENHandler, base=True)
jsonpickle.handlers.register(G2EN, G2ENHandler, base=True)
jsonpickle.handlers.register(GtEN, GtENHandler, base=True)

jsonpickle.handlers.register(G1EP, G1EPHandler, base=True)
jsonpickle.handlers.register(G2EP, G2EPHandler, base=True)
jsonpickle.handlers.register(GtEP, GtEPHandler, base=True)
