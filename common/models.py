from sqlalchemy import ARRAY, Column, MetaData, Text, String, Boolean, DateTime
from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from typing_extensions import Annotated
from datetime import datetime


class Base(DeclarativeBase):
    type_annotation_map = {
        str: Text,
    }
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "%(table_name)s_%(column_0_name)s_key",
            "fk": "%(table_name)s_%(column_0_name)s_fkey",
        }
    )

    def __repr__(self):
        values = {
            col.name: getattr(self, col.name, None) for col in self.__table__.columns
        }
        return f"<{self.__class__.__name__}({values})>"

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
    created_at: Mapped[datetime] = mapped_column(DateTime(True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Group(Base):
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list["User"]] = relationship("User", back_populates="group")
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="group",
        order_by=lambda: [Category.sort_key, Category.id],
    )
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject",
        back_populates="group",
        order_by=lambda: [Subject.sort_key, Subject.id],
    )
    # style related fields
    logo: Mapped[url_type] = mapped_column(nullable=True)
    background: Mapped[url_type] = mapped_column(nullable=True)
    sidebar_show_mode: Mapped[str] = mapped_column(
        nullable=True, server_default="category"
    )  # category or subject


group_foreign_key = Annotated[
    int, mapped_column(ForeignKey(Group.id), index=True, nullable=True)
]

subject_foreign_key = Annotated[
    int, mapped_column(ForeignKey("subject.id"), index=True, nullable=True)
]


class Category(Base):
    id: Mapped[intpk]
    name: Mapped[str]
    sites: Mapped[list["Site"]] = relationship(
        "Site", secondary="category_site_relation", back_populates="categories"
    )
    # the group who can manage this category
    group_id: Mapped[group_foreign_key]
    group: Mapped[Group] = relationship(Group, back_populates="categories")
    subject_id: Mapped[subject_foreign_key]  # just a hint for corresponding subject
    sort_key: Mapped[int] = mapped_column(server_default="0")


cata_fk = Annotated[
    int, mapped_column(ForeignKey(Category.id), index=True, nullable=False)
]


class Site(Base):
    id: Mapped[intpk]
    name: Mapped[str]
    url: Mapped[list[url_type]] = mapped_column(
        ARRAY(String(256)), unique=True, nullable=True
    )
    categories: Mapped[list[Category]] = relationship(
        "Category", secondary="category_site_relation", back_populates="sites"
    )
    pages = relationship("Page", back_populates="site")
    # style related fields
    icon: Mapped[url_type] = mapped_column(nullable=True)
    # the users who want to watch this site
    users = relationship("User", secondary="user_site_relation", back_populates="sites")
    disabled: Mapped[bool] = mapped_column(Boolean, server_default="0")


site_foreign_key = Annotated[
    int, mapped_column(ForeignKey(Site.id), index=True, nullable=False)
]


class Page(Base, UseTimestamps):
    id: Mapped[intpk]
    source_url: Mapped[url_type] = mapped_column(unique=True, nullable=False)

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    title_cn: Mapped[str] = mapped_column(String(128), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    full_content: Mapped[str] = mapped_column(Text, nullable=True)
    full_content_cn: Mapped[str] = mapped_column(Text, nullable=True)
    publish_time: Mapped[datetime] = mapped_column(server_default=func.now())

    score: Mapped[int] = mapped_column(nullable=True, server_default="0")

    site_id: Mapped[site_foreign_key]
    site: Mapped[Site] = relationship(Site, back_populates="pages")

    keywords: Mapped[list["Keyword"]] = relationship(
        "Keyword", secondary="page_keyword_relation", back_populates="pages"
    )

    @hybrid_property
    def school_name(self):
        return self.site.name if self.site else None
    
    @hybrid_property
    def publish_date(self):
        return self.publish_time
    
    @hybrid_property
    def title_raw(self):
        return self.title

    @hybrid_property
    def content_raw(self):
        return self.full_content

    @hybrid_property
    def content_cn(self):
        return self.full_content_cn
    
    @hybrid_property
    def summary_cn(self):
        return self.content


class User(Base):
    id: Mapped[intpk]
    # jaccount_code is used for login
    jaccount_code: Mapped[str] = mapped_column(unique=True, nullable=True)
    # cnaes code
    cnaes_code: Mapped[str] = mapped_column(unique=True, nullable=True)
    # user data
    username: Mapped[str]
    userType: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    organization: Mapped[str] = mapped_column(nullable=True)
    # privilege related fields
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default="0")
    # style related fields
    avatars: Mapped[str] = mapped_column(nullable=True)
    # password
    ## format: f"${salt}-${sha256(salt + password)}"
    password: Mapped[str] = mapped_column(nullable=True)

    #### relationship ####
    group_id: Mapped[group_foreign_key]
    group_accepted: Mapped[bool] = mapped_column(Boolean, server_default="0")
    group_admin: Mapped[bool] = mapped_column(Boolean, server_default="0")
    group: Mapped[Group] = relationship(Group, back_populates="users")
    # the bookmarks the user saved
    bookmarks = relationship("Bookmark", back_populates="user")
    # the keywords the user concern
    keywords: Mapped[list["Keyword"]] = relationship(
        "Keyword", secondary="user_keyword_relation", back_populates="users"
    )
    # the sites the user want to watch
    sites: Mapped[list[Site]] = relationship(
        "Site", secondary="user_site_relation", back_populates="users"
    )


class Bookmark(Base, UseTimestamps):
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    page_id: Mapped[int] = mapped_column(ForeignKey("page.id"), nullable=False)
    user = relationship(User, back_populates="bookmarks")
    page = relationship(Page)


class Subject(Base):
    id: Mapped[intpk]
    name: Mapped[str]
    group_id: Mapped[group_foreign_key]
    group: Mapped[Group] = relationship(Group, back_populates="subjects")
    keywords = relationship(
        "Keyword", secondary="subject_keyword_relation", back_populates="subject"
    )
    sort_key: Mapped[int] = mapped_column(server_default="0")


class Keyword(Base):
    id: Mapped[intpk]
    word: Mapped[str] = mapped_column(unique=True, nullable=False)
    subject = relationship(
        Subject, secondary="subject_keyword_relation", back_populates="keywords"
    )
    pages = relationship(
        Page, secondary="page_keyword_relation", back_populates="keywords"
    )
    users = relationship(
        User, secondary="user_keyword_relation", back_populates="keywords"
    )


class SubjectKeywordRelation(Base):
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subject.id"), nullable=False, primary_key=True
    )
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey("keyword.id"), nullable=False, primary_key=True
    )


class UserKeywordRelation(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False, primary_key=True
    )
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey("keyword.id"), nullable=False, primary_key=True
    )


class PageKeywordRelation(Base):
    page_id: Mapped[int] = mapped_column(
        ForeignKey("page.id"), nullable=False, primary_key=True
    )
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey("keyword.id"), nullable=False, primary_key=True
    )


class UserSiteRelation(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False, primary_key=True
    )
    site_id: Mapped[int] = mapped_column(
        ForeignKey("site.id"), nullable=False, primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), nullable=True, primary_key=True
    )  # allow NULL for independent subscribe
    negative: Mapped[bool] = mapped_column(Boolean, server_default="0")


class CategorySiteRelation(Base):
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), nullable=False, primary_key=True
    )
    site_id: Mapped[int] = mapped_column(
        ForeignKey("site.id"), nullable=False, primary_key=True
    )
