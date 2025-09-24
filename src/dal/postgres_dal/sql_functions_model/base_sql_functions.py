import json
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Any
from uuid import UUID

from asyncpg import Connection

from src.core.logger import logger


class BaseSQLFunctions:
    def __init__(
        self,
        create_function: Optional[str] = None,
        update_function: Optional[str] = None,
        delete_function: Optional[str] = None,
        schema: Optional[str] = None,
    ):
        self.create_function: str = create_function
        self.update_function: str = update_function
        self.delete_function: str = delete_function
        self.schema = schema

    def _qualify(self, function_name: str) -> str:
        if self.schema:
            return f"{self.schema}.{function_name}"
        return function_name

    async def call_create(self, conn: Connection, payload: dict[str, Any]) -> Any:
        if not self.create_function:
            raise NotImplementedError("create function not configured")
        function_name = self._qualify(self.create_function)
        payload_text = self.safe_json_dumps(payload)
        # TODO document function signatures conventions
        new_id = await conn.fetchval(f"SELECT * FROM {function_name}($1::jsonb)", payload_text)
        return {'id': new_id}

    async def call_update(self, conn: Connection, id_value: Any, payload: dict[str, Any]) -> Any:
        if not self.update_function:
            raise NotImplementedError("update function not configured")
        function_name = self._qualify(self.update_function)
        payload_text = self.safe_json_dumps(payload)
        row = await conn.fetchrow(f"SELECT * FROM {function_name}($1, $2::jsonb)", id_value, payload_text)
        return dict(row)

    async def call_delete(self, conn: Connection, id_value: Any) -> Any:
        if not self.delete_function:
            raise NotImplementedError("delete function not configured")
        function_name = self._qualify(self.delete_function)
        row = await conn.fetchrow(f"SELECT * FROM {function_name}($1)", id_value)
        return self._normalize_pg_row(row)

    @staticmethod
    def _normalize_pg_row(row):
        """
        Convert asyncpg.Record (or None) into a python dict or return the raw value.
        Some SQL functions might return a single primitive value or a composite.
        """
        if row is None:
            return None
        try:
            return dict(row)
        except (Exception,):
            logger.error("An error has occurred normalizing function return value")
            return row

    # TODO maybe move this function
    @ staticmethod
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

