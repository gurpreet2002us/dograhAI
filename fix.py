import asyncio
import json
import os
import sys

from api.db import db_client

async def main():
    db_client.init()
    config = await db_client.get_telephony_configuration(1)
    if not config:
        print("Config not found")
        sys.exit(1)
        
    print(f"Old credentials: {config.credentials}")
    
    # Remove api_base if it exists
    new_creds = dict(config.credentials)
    new_creds.pop("api_base", None)
    
    # Update DB
    await db_client.update_telephony_configuration(1, credentials=new_creds)
    print(f"New credentials: {new_creds}")
    print("Done")

if __name__ == "__main__":
    asyncio.run(main())
