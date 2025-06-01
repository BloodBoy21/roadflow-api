#!/usr/bin/env python
"""
Celery worker launcher script
Run this script to start a Celery worker:
    python celery_worker.py
"""

from dotenv import load_dotenv
from lib.mongo import client as mongo_client
from lib.prisma import prisma

# Load environment variables
load_dotenv()

# Import the Celery app and tasks
from lib.celery import celery_app

if __name__ == "__main__":
    print("Starting Celery worker...")
    prisma.connect()
    # The worker will be started using the CLI command
    # This file exists to ensure proper imports and env setup
