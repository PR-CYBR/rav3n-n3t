"""
Core orchestration logic for RavenNet.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from .config import Config
from .pipelines.huginn import HuginnPipeline
from .pipelines.muninn import MuninnPipeline

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class Orchestrator:
    """Main orchestrator for RavenNet framework."""

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the orchestrator.

        Args:
            config: Configuration object (optional, uses defaults if not provided)
        """
        self.config = config or Config()
        self.huginn = HuginnPipeline(self.config)
        self.muninn = MuninnPipeline(self.config)
        self.results = {}

        # Ensure output directory exists
        output_dir = Path(self.config.get("output.directory", "./reports"))
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info("RavenNet Orchestrator initialized")

    def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Run the full pipeline: Huginn → Muninn.

        Returns:
            Dictionary containing results from both pipelines
        """
        logger.info("=" * 80)
        logger.info("Starting RavenNet full pipeline orchestration")
        logger.info("=" * 80)

        start_time = datetime.now()

        try:
            # Run Huginn (Thought) pipeline first
            logger.info("Phase 1: Running Huginn (Thought) pipeline")
            huginn_result = self._run_pipeline("huginn", self.huginn)
            self.results["huginn"] = huginn_result

            # Run Muninn (Memory) pipeline second
            logger.info("Phase 2: Running Muninn (Memory) pipeline")
            muninn_result = self._run_pipeline("muninn", self.muninn)
            self.results["muninn"] = muninn_result

            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()

            self.results["metadata"] = {
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": duration,
                "status": "success",
            }

            logger.info("=" * 80)
            logger.info(f"RavenNet orchestration completed successfully in {duration:.2f}s")
            logger.info("=" * 80)

            return self.results

        except Exception as e:
            logger.error(f"RavenNet orchestration failed: {e}", exc_info=True)

            self.results["metadata"] = {
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - start_time).total_seconds(),
                "status": "failed",
                "error": str(e),
            }

            raise

    def run_pipeline(self, pipeline_name: str) -> Dict[str, Any]:
        """
        Run a specific pipeline by name.

        Args:
            pipeline_name: Name of the pipeline ('huginn' or 'muninn')

        Returns:
            Pipeline execution results
        """
        logger.info(f"Running {pipeline_name} pipeline")

        if pipeline_name.lower() == "huginn":
            return self._run_pipeline("huginn", self.huginn)
        elif pipeline_name.lower() == "muninn":
            return self._run_pipeline("muninn", self.muninn)
        else:
            raise ValueError(f"Unknown pipeline: {pipeline_name}")

    def _run_pipeline(self, name: str, pipeline) -> Dict[str, Any]:
        """
        Internal method to run a pipeline with error handling.

        Args:
            name: Pipeline name
            pipeline: Pipeline instance

        Returns:
            Pipeline execution results
        """
        if not self.config.get(f"pipelines.{name}.enabled", True):
            logger.info(f"{name.capitalize()} pipeline is disabled, skipping")
            return {"status": "skipped", "reason": "disabled"}

        try:
            result = pipeline.run()
            logger.info(f"{name.capitalize()} pipeline completed successfully")
            return result

        except Exception as e:
            logger.error(f"{name.capitalize()} pipeline failed: {e}", exc_info=True)

            retry_count = self.config.get(f"pipelines.{name}.retry_count", 0)

            if retry_count > 0:
                logger.info(f"Retrying {name} pipeline ({retry_count} attempts remaining)")
                # TODO: Implement retry logic

            raise

    def get_results(self) -> Dict[str, Any]:
        """
        Get the results from the last orchestration run.

        Returns:
            Results dictionary
        """
        return self.results
