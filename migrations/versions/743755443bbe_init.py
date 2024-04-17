"""init

Revision ID: 743755443bbe
Revises: 
Create Date: 2024-04-17 16:49:45.818936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743755443bbe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE events (
            event_id VARCHAR,
            event_no SERIAL,
            event_type VARCHAR,
            event_message TEXT,
            PRIMARY KEY ( event_id, event_no )
        );
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION notify_event()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                PERFORM pg_notify('event_insert', NEW.event_id || ',' || NEW.event_no || ',' || NEW.event_type || ',' || NEW.event_message);
            ELSIF TG_OP = 'DELETE' THEN
                PERFORM pg_notify('event_delete', OLD.event_id || ',' || OLD.event_no || ',' || OLD.event_type || ',' || OLD.event_message);
            ELSIF TG_OP = 'UPDATE' THEN
                PERFORM pg_notify('event_update', NEW.event_id || ',' || NEW.event_no || ',' || NEW.event_type || ',' || NEW.event_message);
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER events_notify
        AFTER INSERT OR UPDATE OR DELETE ON events
        FOR EACH ROW
        EXECUTE FUNCTION notify_event();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER events_notify ON events;")
    op.execute("DROP FUNCTION notify_event;")
    op.execute("DROP TABLE events;")
