"""
Pytest configuration and fixtures for LAW-STUDY tests
"""
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.query_planner import (
    extract_keywords,
    expand_synonyms,
    build_query_set,
    _build_admin_law_queries,
    remove_stopwords,
)

# Import for DI container testing
try:
    from core.container import create_container, reset_container, Container
    CONTAINER_AVAILABLE = True
except ImportError:
    CONTAINER_AVAILABLE = False


@pytest.fixture(scope="session")
def test_config():
    """Test configuration"""
    return {
        "LAW_API_KEY": "test_key",
        "PORT": 8099,
        "LOG_LEVEL": "DEBUG"
    }


@pytest.fixture(scope="function")
def container(test_config):
    """DI container for testing"""
    if not CONTAINER_AVAILABLE:
        pytest.skip("DI container not available")
    
    # Create fresh container for each test
    reset_container()
    container = create_container()
    container.config.LAW_API_KEY.from_value(test_config["LAW_API_KEY"])
    
    yield container
    
    # Cleanup
    reset_container()


@pytest.fixture(scope="function")
def precedent_service(container):
    """Precedent service from DI container"""
    if not CONTAINER_AVAILABLE:
        pytest.skip("DI container not available")
    return container.precedent_service()


@pytest.fixture(scope="function")
def law_service(container):
    """Law service from DI container"""
    if not CONTAINER_AVAILABLE:
        pytest.skip("DI container not available")
    return container.law_service()


@pytest.fixture(scope="function")
def compliance_service(container):
    """Compliance service from DI container"""
    if not CONTAINER_AVAILABLE:
        pytest.skip("DI container not available")
    return container.compliance_service()


@pytest.fixture(scope="function")
def health_service(container):
    """Health service from DI container"""
    if not CONTAINER_AVAILABLE:
        pytest.skip("DI container not available")
    return container.health_service()


@pytest.fixture
def sample_admin_queries():
    """Sample administrative law queries for testing"""
    return [
        "행정행위 무효사유 명백성 보충적으로 요구된다",
        "행정처분 하자 중대 명백",
        "원고적격 피고적격 소송요건",
        "재량권 남용 일탈 한계",
        "정보공개청구 비공개 사유",
    ]


@pytest.fixture
def sample_keyword_tests():
    """Test cases for keyword extraction"""
    return [
        # (input, expected_keywords)
        ("행정행위 무효 명백성", ["행정행위", "무효", "명백성"]),
        ("중대하고 명백한 하자", ["중대", "명백", "하자"]),
        ("원고적격이 없다", ["원고적격"]),
        ("재량권 일탈 남용", ["재량권", "일탈", "남용"]),
    ]
