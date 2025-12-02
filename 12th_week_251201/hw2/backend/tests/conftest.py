import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from main import app


@pytest.fixture
def client():
    """FastAPI TestClient 인스턴스"""
    return TestClient(app)
