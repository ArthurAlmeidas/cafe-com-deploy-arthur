import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "cafes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(80), nullable=False, unique=True),
        sa.Column("preco", sa.Numeric(6, 2, asdecimal=False), nullable=False),
    )


def downgrade():
    op.drop_table("cafes")
