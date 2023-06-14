import uvicorn
import socket

from app import create_app

app = create_app()

if __name__ == '__main__':
    inner_ip = socket.gethostbyname(socket.gethostname())
    uvicorn.run(
        app='main:app',
        host=inner_ip,
        port=8788,
        reload=True,
        # log_level='trace',
    )
