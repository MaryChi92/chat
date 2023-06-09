import dis

from types import FunctionType


VERIFICATION_PARAMS = ("accept", "listen", "connect", "AF_INET", "SOCK_STREAM")


class BaseVerifier(type):
    def __init__(cls, name, bases, namespaces):
        super().__init__(name, bases, namespaces)

        arguments = []
        parent_attrs = [base.__dict__ for base in bases]
        for attr_dict in (namespaces, *parent_attrs):
            for value in attr_dict.values():
                if isinstance(value, (FunctionType, staticmethod)):
                    if hasattr(value, "__closure__"):
                        try:
                            args = value.__closure__[0].cell_contents
                        except TypeError:
                            args = value
                    else:
                        args = value
                    arguments.append(args)

        cls.attrs = {f"_{name}_attrs": set()}
        for func in arguments:
            bytecode = dis.Bytecode(func)
            for line in bytecode:
                if line.argval in VERIFICATION_PARAMS:
                    cls.attrs[f"_{name}_attrs"].add(line.argval)

        arguments.clear()

        params = cls.attrs[f"_{name}_attrs"]
        if not ("SOCK_STREAM" in params and "AF_INET" in params):
            raise TypeError("TCP only")
