<%!
def fmt(value):
    """repr(), but preferring double quotes to match the project's style.

    repr() already renders every shape alembic passes here correctly: a str for
    a normal revision, a tuple for a merge revision, None for the first one.
    So only the quote style is adjusted, and only when that cannot corrupt the
    literal (a value already containing a double quote is left to repr).
    """
    text = repr(value)
    return text if '"' in text else text.replace("'", '"')
%>\
"""${message}

Revision ID: ${up_revision}
Revises:${" " + comma(down_revision) if down_revision else ""}
Create Date: ${create_date}

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
% if imports:
${imports}
% endif

# revision identifiers, used by Alembic.
revision: str = ${fmt(up_revision)}
down_revision: str | Sequence[str] | None = ${fmt(down_revision)}
branch_labels: str | Sequence[str] | None = ${fmt(branch_labels)}
depends_on: str | Sequence[str] | None = ${fmt(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
