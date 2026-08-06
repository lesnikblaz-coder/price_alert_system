"""add alert status"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "39e430ad61fd"
down_revision: Union[str, Sequence[str], None] = "bffb1d20cdda"
branch_labels = None
depends_on = None

alert_status = sa.Enum(
    "ACTIVE",
    "TRIGGERED",
    "CANCELLED",
    name="alertstatus",
)


def upgrade() -> None:
    # Create the PostgreSQL enum type
    alert_status.create(op.get_bind(), checkfirst=True)

    # Add the new column with a temporary default for existing rows
    op.add_column(
        "alerts",
        sa.Column(
            "status",
            alert_status,
            nullable=False,
            server_default="ACTIVE",
        ),
    )

    # Remove the server default -> python default already defined in models
    op.alter_column("alerts", "status", server_default=None)

    # Drop the old column
    op.drop_column("alerts", "is_active")


def downgrade() -> None:
    op.add_column(
        "alerts",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.drop_column("alerts", "status")

    # Drop the enum type
    alert_status.drop(op.get_bind(), checkfirst=True)
