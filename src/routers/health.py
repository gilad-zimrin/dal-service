from fastapi import APIRouter

health_router = APIRouter(
    prefix="/health",
)

@health_router.get("/", summary="Basic health check")
async def health():
    """
    Returns simple OK status to verify service is alive.
    """
    return {"status": "ok"}

@health_router.get("/ready", summary="Readiness check")
async def readiness():
    """
    Check if service is ready (e.g., DB connection available)
    """
    # For now just return OK; later you can add async checks to DB/Redis/etc.
    return {"status": "ready"}
