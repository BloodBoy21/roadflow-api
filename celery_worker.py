#!/usr/bin/env python
"""
Celery worker launcher script
Run this script to start a Celery worker:
    celery -A celery_worker.celery_app worker --loglevel=info
"""

from dotenv import load_dotenv

from lib.celery import celery_app  # noqa: F401
from lib.prisma import prisma

# Load environment variables
load_dotenv()

# Import tasks to register them with Celery
import services.celery_jobs.tasks  # noqa: F401

if __name__ == "__main__":
    print("Starting Celery worker...")
    prisma.connect()
    # The worker will be started using the CLI command
    # This file exists to ensure proper imports and env setup
