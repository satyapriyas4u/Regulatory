from fastapi import APIRouter
# from regulatory.services.generator import generate_device_input_section  # from src/regulatory

router = APIRouter()

@router.post("/generate")
async def generate(req: dict):
    return print("generate_device_input_section(req)")
