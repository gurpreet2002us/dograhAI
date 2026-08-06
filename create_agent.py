import asyncio
from sqlalchemy import select
from api.db import db_client
from api.db.database import async_session
from api.db.models import UserModel
import uuid
import json

async def main():
    async with async_session() as session:
        result = await session.execute(select(UserModel).where(UserModel.email == "gurpreet2002in@gmail.com"))
        user = result.scalars().first()
        
        if not user:
            print("User not found!")
            return

        agent_prompt = """# Goal
You are an expert sales representative for a modern dine-in ordering software called 'DineFlow'. Your goal is to explain our features, compare us to competitors, collect the caller's details, and schedule a demo if they are interested. 

## Core Features to mention:
1. QR Code Ordering & Payments
2. Real-time Kitchen Display System (KDS)
3. POS Integration
4. Live Inventory Tracking
5. Waitlist & Reservation Management
6. Customer Loyalty Programs
7. Multi-location Support
8. AI-driven Analytics Dashboard
9. Staff Management & Scheduling
10. Automated SMS Marketing

## Competitor Differentiation:
We offer 0% commission on orders, integrate directly with existing POS hardware without needing new tablets, and provide 24/7 localized support unlike other major providers in the market.

## Call Flow:
1. Greet the user warmly and introduce yourself as a DineFlow expert.
2. Ask about their restaurant and explain features based on their pain points.
3. If they are interested, ask for their name, phone number, and preferred demo time.
4. Tell them you have scheduled a demo and they will receive a WhatsApp/SMS confirmation.
"""

        workflow_def = {
            "nodes": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "startCall",
                    "position": {"x": 175, "y": 60},
                    "data": {
                        "prompt": agent_prompt,
                        "name": "start call",
                        "allow_interrupt": True,
                        "add_global_prompt": False,
                        "delayed_start": False,
                        "is_start": True,
                        "extraction_enabled": False,
                        "greeting_type": "text",
                        "greeting": "Hello, thanks for calling DineFlow! Are you looking to upgrade your restaurant's ordering system today?",
                        "delayed_start_duration": 2,
                        "pre_call_fetch_enabled": False
                    }
                }
            ],
            "edges": [],
            "viewport": {"x": 582.0, "y": 121.5, "zoom": 0.75}
        }
        
        workflow = await db_client.create_workflow(
            name="Dine-in Sales Agent",
            workflow_definition=workflow_def,
            user_id=user.id,
            organization_id=user.selected_organization_id
        )
        print(f"Created workflow successfully! ID: {workflow.id}")

if __name__ == "__main__":
    asyncio.run(main())
