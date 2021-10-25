import uvicorn
from app.main import app  # MUST
from app.core.config import config


if __name__ == "__main__":
    uvicorn.run("run_server:app", host=config.SERVER_HOST, port=config.SERVER_PORT, reload=False)
