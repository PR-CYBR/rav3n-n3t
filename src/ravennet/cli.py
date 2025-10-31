"""
CLI interface for RavenNet.
"""

import argparse
import sys
import logging
from pathlib import Path

from . import Orchestrator, Config, __version__

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RavenNet - Central orchestration hub for rav3n-n3t framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"RavenNet {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run orchestration")
    run_parser.add_argument(
        "--pipeline",
        choices=["huginn", "muninn"],
        help="Run only a specific pipeline (default: run both)",
    )
    run_parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
    )
    run_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Check status of last run")
    status_parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file",
    )

    args = parser.parse_args()

    # Set logging level
    if hasattr(args, "verbose") and args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return 0

    try:
        if args.command == "run":
            return run_command(args)
        elif args.command == "status":
            return status_command(args)
        else:
            parser.print_help()
            return 1

    except Exception as e:
        logger.error(f"Command failed: {e}", exc_info=True)
        return 1


def run_command(args):
    """Execute the run command."""
    # Load configuration
    config = Config(args.config) if args.config else Config()

    # Create orchestrator
    orchestrator = Orchestrator(config)

    try:
        if args.pipeline:
            # Run specific pipeline
            logger.info(f"Running {args.pipeline} pipeline only")
            result = orchestrator.run_pipeline(args.pipeline)
            # For single pipeline runs, check status directly
            if result.get("status") == "success":
                logger.info("✓ Orchestration completed successfully")
                return 0
            else:
                logger.error("✗ Orchestration completed with errors")
                return 1
        else:
            # Run full pipeline
            result = orchestrator.run_full_pipeline()
            # For full pipeline, check metadata status
            if result.get("metadata", {}).get("status") == "success":
                logger.info("✓ Orchestration completed successfully")
                return 0
            else:
                logger.error("✗ Orchestration completed with errors")
                return 1

    except Exception as e:
        logger.error(f"✗ Orchestration failed: {e}")
        return 1


def status_command(args):
    """Execute the status command."""
    config = Config(args.config) if args.config else Config()
    output_dir = Path(config.get("output.directory", "./reports"))

    if not output_dir.exists():
        print("No reports directory found. Run 'ravennet run' first.")
        return 1

    # TODO: Implement status checking logic in Phase 2
    print("Status command - implementation coming in Phase 2")
    print(f"Reports directory: {output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
