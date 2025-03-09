import os
from sqlalchemy import select, asc, desc
from fastapi.concurrency import run_in_threadpool
from app.database import ImageOrm, new_session
from app.schemas import SImageAdd, SImage

class ImageRepository:
    @classmethod
    async def add_image(cls, image: SImageAdd) -> int:
        async with new_session() as session:
            data = image.model_dump()
            new_image = ImageOrm(**data)
            session.add(new_image)
            await session.flush()
            await session.commit()
            return new_image.id

    @classmethod
    async def get_images(cls) -> list[SImage]:
        async with new_session() as session:
            query = select(ImageOrm)
            result = await session.execute(query)
            image_models = result.scalars().all()
            images = []
            for image_model in image_models:
                image_data = image_model.__dict__
                image_data.pop('_sa_instance_state', None)
                images.append(SImage(**image_data))
            return images

    @classmethod
    async def get_image_by_id(cls, image_id: int) -> SImage | None:
        async with new_session() as session:
            query = select(ImageOrm).where(ImageOrm.id == image_id)
            result = await session.execute(query)
            image_model = result.scalar_one_or_none()
            if image_model:
                image_data = image_model.__dict__
                image_data.pop('_sa_instance_state', None)
                return SImage(**image_data)
            return None

    @classmethod
    async def delete_image(cls, image_id: int) -> bool:
        async with new_session() as session:
            query = select(ImageOrm).where(ImageOrm.id == image_id)
            result = await session.execute(query)
            image_model = result.scalar_one_or_none()

            if image_model:
                image_path = image_model.image_path
                preview_path = image_model.preview_path
                embedding_path = image_model.embedding_path

                await session.delete(image_model)
                await session.commit()

                if os.path.exists(image_path):
                    await run_in_threadpool(os.remove, image_path)
                if os.path.exists(preview_path):
                    await run_in_threadpool(os.remove, preview_path)
                if os.path.exists(embedding_path):
                    await run_in_threadpool(os.remove, embedding_path)

                return True
            return False
    

    @classmethod
    async def delete_all_images(cls) -> int:
        async with new_session() as session:
            query = select(ImageOrm)
            result = await session.execute(query)
            image_models = result.scalars().all()

            if not image_models:
                return 0

            count_deleted = 0
            for image_model in image_models:
                image_path = image_model.image_path
                preview_path = image_model.preview_path
                embedding_path = image_model.embedding_path

                await session.delete(image_model)
                count_deleted += 1

                if os.path.exists(image_path):
                    await run_in_threadpool(os.remove, image_path)
                if os.path.exists(preview_path):
                    await run_in_threadpool(os.remove, preview_path)
                if os.path.exists(embedding_path):
                    await run_in_threadpool(os.remove, embedding_path)
            await session.commit()
            return count_deleted
