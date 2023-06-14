from fastapi import FastAPI
from app.router import init_router


async def handle_startup():
    print('on_startup')


async def handle_shutdown():
    print('on_shutdown')


def create_app():
    app = FastAPI(
        title='API server for pay platform',
        description='支付平台后端接口',
        version='0.0.1',
        on_startup=[handle_startup],
        on_shutdown=[handle_shutdown]
    )

    init_router(app)

    return app
