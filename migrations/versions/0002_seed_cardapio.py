import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

CAFES = [
    {"nome": "Espresso", "preco": 6.50},
    {"nome": "Cappuccino", "preco": 10.00},
    {"nome": "Café Coado", "preco": 5.00},
    {"nome": "Latte", "preco": 11.00},
    {"nome": "Mocha", "preco": 12.50},
    {"nome": "Cold Brew", "preco": 13.00},
]


def upgrade():
    tabela = sa.table("cafes", sa.column("nome", sa.String), sa.column("preco", sa.Numeric))
    op.bulk_insert(tabela, CAFES)


def downgrade():
    nomes = ", ".join(f"'{c['nome']}'" for c in CAFES)
    op.execute(f"DELETE FROM cafes WHERE nome IN ({nomes})")
