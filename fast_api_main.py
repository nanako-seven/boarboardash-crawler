from fastapi import FastAPI, Request

app = FastAPI()


@app.post('/test')
async def test_api(req: Request):
    json = await req.json()
    print(json)
    return {'status': 'ok'}
