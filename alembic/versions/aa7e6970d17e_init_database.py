"""init database

Revision ID: aa7e6970d17e
Revises: 
Create Date: 2025-08-07 15:02:09.409479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7e6970d17e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('utilisateur',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('bio', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=32), nullable=True),
    sa.Column('gender', sa.String(length=32), nullable=True),
    sa.Column('profile_picture', sa.String(length=255), nullable=True, server_default='default.jpg'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True, server_default=sa.text('false')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('follow',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['utilisateur.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('follower_id', 'followed_id', name='unique_follow')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('caption', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('hidden_tag', sa.Boolean(), nullable=True, server_default=sa.text('false')),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('conversation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user1_id', sa.Integer(), nullable=False),
    sa.Column('user2_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user1_id'], ['utilisateur.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user1_id', 'user2_id', name='unique_conversation')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('like',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'post_id', name='unique_like')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['utilisateur.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('conversation_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True, server_default=sa.text('false')),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('message')
    op.drop_table('notification')
    op.drop_table('like')
    op.drop_table('comment')
    op.drop_table('conversation')
    op.drop_table('post')
    op.drop_table('follow')
    op.drop_table('utilisateur')
