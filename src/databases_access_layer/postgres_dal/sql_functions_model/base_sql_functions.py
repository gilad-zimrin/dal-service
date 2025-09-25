from typing import Optional, Any

from asyncpg import Connection

from src.core.safe_json_converter import safe_json_dumps


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
        payload_text = safe_json_dumps(payload)
        # TODO document function signatures conventions
        new_id = await conn.fetchval(f"SELECT * FROM {function_name}($1::jsonb)", payload_text)
        return {'id': new_id}

    async def call_update(self, conn: Connection, id_value: Any, payload: dict[str, Any]) -> Any:
        if not self.update_function:
            raise NotImplementedError("update function not configured")
        function_name = self._qualify(self.update_function)
        payload_text = safe_json_dumps(payload)
        row = await conn.fetchrow(f"SELECT * FROM {function_name}($1, $2::jsonb)", id_value, payload_text)
        return dict(row)

    async def call_delete(self, conn: Connection, id_value: Any) -> Any:
        if not self.delete_function:
            raise NotImplementedError("delete function not configured")
        function_name = self._qualify(self.delete_function)
        row = await conn.fetchrow(f"SELECT * FROM {function_name}($1)", id_value)
        return row
