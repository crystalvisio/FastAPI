from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.schema import PrimaryKeyConstraint

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="posts")
    votes = relationship("Vote", back_populates="post")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, unique=True, index=True)  # Renamed to `name`

    # Relationship to User
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(255), nullable=False)  
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    is_active = Column(Boolean, server_default=text("TRUE"))  # Changed to `True` for clarity
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # Ensured role_id is non-nullable

    posts = relationship("Post", back_populates="user")
    votes = relationship("Vote", back_populates="user")
    role = relationship("Role", back_populates="users")


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    vote_dir = Column(Integer, nullable=False)

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")

    __table_args__ = (PrimaryKeyConstraint("post_id", "user_id"),)