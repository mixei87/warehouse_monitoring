from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repo.movement import MovementRepository
from app.repo.product import ProductRepository
from app.repo.stock import StockRepository
from app.repo.warehouse import WarehouseRepository
from app.services.movement import MovementService
from app.services.stock import StockService
from app.services.warehouse import WarehouseService


# Зависимости репозиториев
async def get_warehouse_repo(db: AsyncSession = Depends(get_db)) -> WarehouseRepository:
    return WarehouseRepository(db=db)


async def get_stock_repo(db: AsyncSession = Depends(get_db)) -> StockRepository:
    return StockRepository(db=db)


async def get_movement_repo(db: AsyncSession = Depends(get_db)) -> MovementRepository:
    return MovementRepository(db=db)


async def get_product_repo(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db=db)


# Зависимости сервисов
async def get_warehouse_service(
    db: AsyncSession = Depends(get_db),
    warehouse_repo: WarehouseRepository = Depends(get_warehouse_repo),
) -> WarehouseService:
    return WarehouseService(db=db, warehouse_repo=warehouse_repo)


async def get_movement_service(
    db: AsyncSession = Depends(get_db),
    movement_repo: MovementRepository = Depends(get_movement_repo),
    warehouse_service: WarehouseService = Depends(get_warehouse_service),
) -> MovementService:
    return MovementService(
        db=db, movement_repo=movement_repo, warehouse_service=warehouse_service
    )


async def get_stock_service(
    db: AsyncSession = Depends(get_db),
    stock_repo: StockRepository = Depends(get_stock_repo),
    warehouse_repo: WarehouseRepository = Depends(get_warehouse_repo),
    product_repo: ProductRepository = Depends(get_product_repo),
) -> StockService:
    return StockService(
        db=db,
        stock_repo=stock_repo,
        warehouse_repo=warehouse_repo,
        product_repo=product_repo,
    )


WarehouseServiceDepends = Annotated[WarehouseService, Depends(get_warehouse_service)]
MovementServiceDepends = Annotated[MovementService, Depends(get_movement_service)]
StockServiceDepends = Annotated[StockService, Depends(get_stock_service)]
