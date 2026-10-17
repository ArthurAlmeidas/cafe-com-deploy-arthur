import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("cafes", sa.Column("origem", sa.String(80), nullable=True))


def downgrade():
    op.drop_column("cafes", "origem")