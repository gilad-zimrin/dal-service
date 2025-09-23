# TODO create an alembic script for postgres database migrations
from alembic import op
import pathlib

# revision identifiers, used by Alembic.
revision = "123456789abc"
down_revision = "<previous_rev>"
branch_labels = None
depends_on = None

# Explicit list of .sql files to apply
SQL_FILES = [
    "migrations/sql/user_functions.sql",
    "migrations/sql/item_functions.sql",
]

def upgrade():
    for file_path in SQL_FILES:
        sql_file = pathlib.Path(file_path)
        if not sql_file.exists():
            raise RuntimeError(f"Missing SQL file {sql_file}")
        op.execute(sql_file.read_text())


def downgrade():
    # explicitly drop the functions created above
    # (Alembic cannot auto-reverse SQL, so we must list them)
    op.execute("DROP FUNCTION IF EXISTS app.user_create(jsonb);")
    op.execute("DROP FUNCTION IF EXISTS app.user_update(jsonb);")
    op.execute("DROP FUNCTION IF EXISTS app.user_delete(bigint);")

    op.execute("DROP FUNCTION IF EXISTS app.item_create(jsonb);")
    op.execute("DROP FUNCTION IF EXISTS app.item_update(jsonb);")
    op.execute("DROP FUNCTION IF EXISTS app.item_delete(bigint);")
