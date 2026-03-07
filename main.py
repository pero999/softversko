from fastapi import FastAPI

app = FastAPI(
    title="Softversko API",
    description="FastAPI projekt",
    version="0.1.0",
)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Dobrodošli u Softversko API!"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
