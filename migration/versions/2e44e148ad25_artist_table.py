"""artist_table

Revision ID: 2e44e148ad25
Revises: 736850cd3c1e
Create Date: 2024-12-15 18:00:44.528053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit

# revision identifiers, used by Alembic.
revision: str = '2e44e148ad25'
down_revision: Union[str, None] = '736850cd3c1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE artists (
            id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
            name VARCHAR(255) NOT NULL UNIQUE
        );  
        """
    )
    genre_columns_types = {
        'id' : int,
        'name' : str
    }
    genres = TableInit.parse_data('./migration/versions/csv_data/artist.csv', genre_columns_types, ignore_rows = [0])
    for genre in genres:
        op.execute(
            sa.text("INSERT INTO artists (name) VALUES (:name)").params(genre)
        )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE artists;
        """
    )