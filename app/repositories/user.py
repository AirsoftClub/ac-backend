from sqlalchemy import select

from app.core.exceptions import ResourceNotFound
from app.models import User
from app.repositories.base import BaseRepository
from app.schemas import UserSchema


class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id).where(User.deleted_at.is_(None))
        user = (await self.session.execute(stmt)).scalars().first()
        if not user:
            raise ResourceNotFound("user")
        return user

    async def create(self, user_data: UserSchema) -> User:
        """
        Create a new user in the database
        with all the info retrieved from the UserSchema
        """
        user = User(**user_data.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User:
        """
        Get a user from the database given an email
        """
        stmt = select(User).where(User.email == email).where(User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise ResourceNotFound("user")

        return user

    async def create_or_update(self, user_data: UserSchema) -> User:
        """
        Try to get a user from the database given an email,
        if it exists: we update it, otherwise we create a new user
        """
        try:
            user = await self.get_by_email(user_data.email)
        except ResourceNotFound:
            return await self.create(user_data)

        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.image = user_data.image
        user.email = user_data.email

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
