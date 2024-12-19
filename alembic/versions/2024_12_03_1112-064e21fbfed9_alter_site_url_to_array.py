"""alter site.url to array

Revision ID: 064e21fbfed9
Revises: acdd61a2d114
Create Date: 2024-12-03 11:12:32.921282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '064e21fbfed9'
down_revision: Union[str, None] = 'acdd61a2d114'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加一个临时列来存储数组类型数据
    op.add_column('site', sa.Column('url_temp', sa.ARRAY(sa.String(length=256)), nullable=True))
    
    # 将原列的数据转换并插入到新列
    op.execute("""
        UPDATE site
        SET url_temp = ARRAY[url] -- 假设原来的 `url` 列包含逗号分隔的字符串
    """)
    
    # 删除旧的 `url` 列
    op.drop_column('site', 'url')
    
    # 重命名 `url_temp` 列为 `url`
    op.alter_column('site', 'url_temp', new_column_name='url')


def downgrade() -> None:
    op.add_column('site', sa.Column('url_temp', sa.VARCHAR(length=2048), nullable=True))
    
    op.execute("""
        UPDATE site
        SET url_temp = url[1] -- 假设数组的第一个元素为你想恢复的字符串
    """)
    
    op.drop_column('site', 'url')
    
    op.alter_column('site', 'url_temp', new_column_name='url')
