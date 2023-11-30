import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.configurationdto import ConfigurationCreate
from app.schemas.scopedto import ScopeUpdate, ScopeCreate
from app.schemas.userdto import UserCreate
from app.services.configuration_service import read_configurations, create_configuration
from app.services.scope_service import read_scopes, create_scope
from app.services.user_service import create_user, read_user_by_email

logger = logging.getLogger(__name__)

async def init_db(session: AsyncSession):
    await create_scopes(session)
    await create_superuser(session)
    await create_initial_password(session)
    await session.commit()

async def create_scopes(session: AsyncSession):
    scopes = await read_scopes(session)
    if not scopes:
        userScope = ScopeCreate(
            permission="user",
            description="normal user"
        )
        amdinScope = ScopeCreate(
            permission="admin",
            description="administrator"
        )
        await create_scope(session, userScope)
        await create_scope(session, amdinScope)
        logger.debug("Created scopes [user, admin]")

async def create_superuser(session: AsyncSession):
    superuser = await read_user_by_email(session, "superuser@agilesoda.ai")
    if not superuser:
        user = UserCreate(
            name="superuser",
            email="superuser@agilesoda.ai",
            password="superuser$01",
            scopes=[
                ScopeUpdate(
                    permission="admin",
                    description="administrator",
                    id=2
                )
            ],
            is_active=True
        )
        logger.debug(f"user = {user}")
        result = await create_user(session, user)
        logger.debug("Created a superuser")

async def create_initial_password(session: AsyncSession):
    init_password = await read_configurations(session, key= "initial_password")
    if not init_password:
        config = ConfigurationCreate(
            key ="initial_password",
            value="agilesoda$01",
            description="default password"

        )
        result = await create_configuration(session, config)
        logger.debug("Create a initial password")
