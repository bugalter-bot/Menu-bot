
import asyncpg
from config import DATABASE_URL

pool: asyncpg.Pool | None = None

DEFAULT_CATEGORIES = ["Quyuq", "Suyuq", "Hamirli"]


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, ssl="require")
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS foods (
                id SERIAL PRIMARY KEY,
                category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                image_file_id TEXT,
                recipe TEXT,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        for name in DEFAULT_CATEGORIES:
            await conn.execute(
                "INSERT INTO categories (name) VALUES ($1) ON CONFLICT (name) DO NOTHING",
                name,
            )


async def close_db():
    if pool:
        await pool.close()


# ---------- categories ----------

async def get_categories():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM categories ORDER BY id")


async def get_category(category_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM categories WHERE id=$1", category_id)


async def add_category(name: str):
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "INSERT INTO categories (name) VALUES ($1) ON CONFLICT (name) DO NOTHING RETURNING *",
            name,
        )


async def delete_category(category_id: int):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM categories WHERE id=$1", category_id)


# ---------- foods ----------

async def get_foods_by_category(category_id: int):
    async with pool.acquire() as conn:
        return await conn.fetch(
            "SELECT * FROM foods WHERE category_id=$1 ORDER BY name", category_id
        )


async def get_all_foods():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM foods ORDER BY name")


async def get_food(food_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM foods WHERE id=$1", food_id)


async def add_food(category_id: int, name: str, image_file_id, recipe):
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            """INSERT INTO foods (category_id, name, image_file_id, recipe)
               VALUES ($1, $2, $3, $4) RETURNING *""",
            category_id, name, image_file_id, recipe,
        )


async def update_food_field(food_id: int, field: str, value):
    assert field in ("name", "image_file_id", "recipe")
    async with pool.acquire() as conn:
        await conn.execute(f"UPDATE foods SET {field}=$1 WHERE id=$2", value, food_id)


async def delete_food(food_id: int):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM foods WHERE id=$1", food_id)


async def search_foods(query: str):
    async with pool.acquire() as conn:
        return await conn.fetch(
            "SELECT * FROM foods WHERE name ILIKE $1 ORDER BY name", f"%{query}%"
        )


async def get_random_food(category_id: int | None = None):
    async with pool.acquire() as conn:
        if category_id:
            return await conn.fetchrow(
                "SELECT * FROM foods WHERE category_id=$1 ORDER BY random() LIMIT 1",
                category_id,
            )
        return await conn.fetchrow("SELECT * FROM foods ORDER BY random() LIMIT 1")


# ---------- backup (Excel uchun) ----------

async def get_export_data(category_id: int | None = None):
    """Excel backup uchun (bo'lim, taom nomi, retsept) qatorlarini qaytaradi."""
    async with pool.acquire() as conn:
        if category_id:
            return await conn.fetch(
                """SELECT c.name AS category, f.name, f.recipe
                   FROM foods f JOIN categories c ON c.id = f.category_id
                   WHERE f.category_id = $1
                   ORDER BY f.name""",
                category_id,
            )
        return await conn.fetch(
            """SELECT c.name AS category, f.name, f.recipe
               FROM foods f JOIN categories c ON c.id = f.category_id
               ORDER BY c.name, f.name"""
        )
    data = [dict(r) for r in rows]
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)
