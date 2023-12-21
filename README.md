## Create virtual environment
```bash
python3 -m venv fvenv
```

## activate virtual environment
```bash
source fvenv/bin/activate
```

## install requirements
```bash
pip install -r requirements.txt
```

## run
```bash
flask --app main --debug run --port 5000 --reload
```