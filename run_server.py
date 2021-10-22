import uvicorn
from app.main import app  # MUST
from app.core.config import SERVER_HOST, SERVER_PORT


if __name__ == "__main__":
    uvicorn.run("run_server:app", host=SERVER_HOST, port=SERVER_PORT, reload=False)
