# Plant AI Backend (FastAPI)

A minimal, production-ready FastAPI service for MobileNetV2 plant species inference.

## Features
- `/health` for readiness
- `/metadata/classes` to list class names
- `/predict` (multipart image upload) with `topk` and `threshold`
- `/predict-url` to fetch and classify an image by URL
- `/feedback` endpoint stub for human-in-the-loop corrections
- Temperature scaling support via `TEMPERATURE` env var

## Expected files
Place your trained weights and class mapping here (or set env vars):
```
./weights/final_model.pth
./weights/class_mapping.json
```

Alternatively, set environment variables:
- `MODEL_WEIGHTS=/abs/path/to/model.pth`
- `CLASS_MAPPING_PATH=/abs/path/to/class_mapping.json`
- `MODEL_TYPE=state_dict` or `script`
- `DEVICE=cuda` or `cpu`
- `IMG_SIZE=224`
- `TOPK_DEFAULT=3`
- `TEMPERATURE=1.0`

## Local dev
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Put weights
mkdir -p weights
cp /path/to/final_model.pth weights/
cp /path/to/class_mapping.json weights/

# Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker
```bash
docker build -t plant-ai-backend .
docker run -it --rm -p 8000:8000   -e MODEL_WEIGHTS=/app/weights/final_model.pth   -e CLASS_MAPPING_PATH=/app/weights/class_mapping.json   -v $(pwd)/weights:/app/weights   plant-ai-backend
```

## Example request
```bash
curl -X POST "http://localhost:8000/predict"   -F "file=@/path/to/leaf.jpg"   -F "topk=3" -F "threshold=0.10"
```
