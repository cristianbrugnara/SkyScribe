import jwt
from datetime import datetime, timedelta
import asyncio
from postgrest import AsyncPostgrestClient

secret_key = ''

async def generate_jwt():
    expiration_time = datetime.utcnow() + timedelta(minutes=5)

    payload = {
        'sub': 'user123',
        'exp': expiration_time,
        'iat': datetime.utcnow(),
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

async def main():
    jwt_token = await generate_jwt()

    async with AsyncPostgrestClient("http://37.179.46.148:3001", headers={'Authorization': f'Bearer {jwt_token}'}) as client:
        r = await client.from_("reporting_raw_data").select("pin", "doublevalue", "ts").limit(500).execute()
        raw_data = r.data
        for value in raw_data:
            print(value)

if __name__ == "__main__":
    asyncio.run(main())
