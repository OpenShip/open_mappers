import attr
import json
import types
from typing import Union, Any, TypeVar, Callable

T = TypeVar("T")


class DICTPARSE:

    @staticmethod
    def jsonify(entity: Union[dict, T]) -> str:
        """Return a JSON.

        recursively parse a data type using __dict__ into a JSON
        """

        def _parser(item):
            if attr.has(item):
                if isinstance(item, Callable):
                    return item.__name__
                return attr.asdict(item)
            if isinstance(item, types.FunctionType):
                return None
            if isinstance(item, type):
                return str(item)
            if isinstance(item, Callable):
                return str(item)
            if hasattr(item, "__dict__"):
                return item.__dict__

            return item

        return json.dumps(
            entity,
            default=_parser,
            sort_keys=True,
            indent=4,
        )

    @staticmethod
    def to_dict(entity: Any) -> dict:
        """Return a python dictionary.

        recursively parse a data type using __dict__ into a JSON
        """
        return json.loads(
            DICTPARSE.jsonify(entity) if not isinstance(entity, str) else entity,
            object_hook=lambda d: {k: v for k, v in d.items() if v not in (None, [], "")},
        )

