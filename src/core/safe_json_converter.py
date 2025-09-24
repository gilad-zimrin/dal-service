import json
from datetime import datetime, date
from decimal import Decimal
from typing import Any
from uuid import UUID


def safe_json_dumps(data: dict[str, Any], **json_kwargs) -> str:
    """
        Safely JSON-serialize a dictionary.

        Any value not natively JSON-serializable is converted:
        - datetime/date -> ISO 8601 string
        - Decimal -> float
        - UUID -> string
        - Other unknown types -> string via str()

        :param data: Dictionary to serialize
        :param json_kwargs: Extra kwargs passed to json.dumps
        :return: JSON string
        """

    def default_converter(obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)
        return str(obj)

    return json.dumps(data, default=default_converter, ensure_ascii=False, **json_kwargs)