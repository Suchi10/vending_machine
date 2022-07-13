import uvicorn
from fastapi import FastAPI

from app.routes import product, user

DESCRIPTION = """
Vending Machine is a service that is responsible for saving the product and user details.
"""

app = FastAPI(
    title="Vending Machine",
    description=DESCRIPTION,
    version="1.0",
)

app.include_router(product.router)
app.include_router(user.router)


@app.get("/health")
def health():
    return "Healthy!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
