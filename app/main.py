import uvicorn
import graph

from fastapi import FastAPI

app = FastAPI()
app.include_router(graph.router)

if __name__ == "__main__":
    uvicorn.run(app)
