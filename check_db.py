import asyncio
from dotenv import load_dotenv
load_dotenv('api/.env')
from api.db import db_client
from sqlalchemy import text

async def main():
    async with db_client.async_session() as session:
        res = await session.execute(text("SELECT id, address, address_normalized, is_active, inbound_workflow_id FROM telephony_phone_numbers"))
        for row in res.fetchall():
            print(row)

asyncio.run(main())
