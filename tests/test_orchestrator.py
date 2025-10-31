"""
Basic tests for RavenNet orchestrator.
"""

import pytest
from ravennet import Orchestrator, Config


def test_config_initialization():
    """Test that Config can be initialized."""
    config = Config()
    assert config is not None
    assert config.get("pipelines.huginn.enabled") is True
    assert config.get("pipelines.muninn.enabled") is True


def test_orchestrator_initialization():
    """Test that Orchestrator can be initialized."""
    orchestrator = Orchestrator()
    assert orchestrator is not None
    assert orchestrator.config is not None
    assert orchestrator.huginn is not None
    assert orchestrator.muninn is not None


def test_config_get_set():
    """Test config get/set methods."""
    config = Config()

    # Test get
    assert config.get("pipelines.huginn.timeout") == 3600

    # Test set
    config.set("pipelines.huginn.timeout", 7200)
    assert config.get("pipelines.huginn.timeout") == 7200

    # Test default value
    assert config.get("nonexistent.key", "default") == "default"


def test_pipeline_run():
    """Test that pipelines can run."""
    orchestrator = Orchestrator()

    # Test Huginn pipeline
    huginn_result = orchestrator.run_pipeline("huginn")
    assert huginn_result["status"] == "success"
    assert huginn_result["pipeline"] == "huginn"

    # Test Muninn pipeline
    muninn_result = orchestrator.run_pipeline("muninn")
    assert muninn_result["status"] == "success"
    assert muninn_result["pipeline"] == "muninn"


def test_full_pipeline():
    """Test full pipeline orchestration."""
    orchestrator = Orchestrator()
    results = orchestrator.run_full_pipeline()

    assert "huginn" in results
    assert "muninn" in results
    assert "metadata" in results

    assert results["huginn"]["status"] == "success"
    assert results["muninn"]["status"] == "success"
    assert results["metadata"]["status"] == "success"


def test_invalid_pipeline():
    """Test that invalid pipeline names raise errors."""
    orchestrator = Orchestrator()

    with pytest.raises(ValueError):
        orchestrator.run_pipeline("invalid_pipeline")
