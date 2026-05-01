import aiomysql
import asyncio

class Database:
    def __init__(self, host, database, username, password):
        self.host = host
        self.database = database
        self.username = username
        self.password = password

    async def connect(self):
        try:
            self.conn = await aiomysql.create_pool(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password
            )
            print("Database connected successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    async def execute_query(self, query, params=None):
        if params is None:
            params = []
        async with self.conn.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchall()
                return result

    async def close(self):
        await self.conn.close()

async def get_db():
    try:
        db = Database('your_host', 'your_database', 'your_username', 'your_password')
        await db.connect()
        return db
    except Exception as e:
        print(f"Error initializing database connection: {e}")
        return None