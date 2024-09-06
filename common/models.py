from sqlalchemy import Text, String, Boolean
from sqlalchemy import ForeignKey, Text, func

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from typing_extensions import Annotated

from datetime import datetime


class Base(DeclarativeBase):
    type_annotation_map = {
        str: Text,
    }

    def __init_subclass__(cls) -> None:
        if "__tablename__" not in cls.__dict__:
            name = ""
            for c in cls.__name__:
                if c.isupper():
                    if name != "":
                        name += "_"
                name += c.lower()
            setattr(cls, "__tablename__", name)
        return super().__init_subclass__()


metadata = Base.metadata  # used for alembic

intpk = Annotated[int, mapped_column(primary_key=True)]
url_type = Annotated[str, mapped_column(String(2048))]


class UseTimestamps:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Category(Base):
    id: Mapped[intpk]
    name: Mapped[str]
    sites = relationship("Site", back_populates="category")


cata_fk = Annotated[
    int, mapped_column(ForeignKey(Category.id), index=True, nullable=False)
]


class Site(Base):
    id: Mapped[intpk]
    name: Mapped[str]
    url: Mapped[url_type] = mapped_column(unique=True, nullable=False)
    cate_id: Mapped[cata_fk]
    category: Mapped[Category] = relationship(Category, back_populates="sites")
    pages = relationship("Page", back_populates="site")
    # style related fields
    icon: Mapped[url_type] = mapped_column(nullable=True)


site_foreign_key = Annotated[
    int, mapped_column(ForeignKey(Site.id), index=True, nullable=False)
]


class Page(Base, UseTimestamps):
    id: Mapped[intpk]
    source_url: Mapped[url_type] = mapped_column(unique=True, nullable=False)

    title = mapped_column(String(128), nullable=False)
    content = mapped_column(Text, nullable=False)
    full_content = mapped_column(Text, nullable=True)
    publish_time: Mapped[datetime] = mapped_column(server_default=func.now())

    site_id: Mapped[site_foreign_key]
    site: Mapped[Site] = relationship(Site, back_populates="pages")

    cate_id: Mapped[cata_fk]
    category = relationship(Category)


class User(Base):
    id: Mapped[intpk]
    # jaccount_code is used for login
    jaccount_code: Mapped[str] = mapped_column(unique=True, nullable=False)
    # user data
    username: Mapped[str]
    userType: Mapped[str]
    name: Mapped[str]
    organization: Mapped[str]
    # privilege related fields
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default="0")
    # style related fields
    avatars: Mapped[str] = mapped_column(nullable=True)
