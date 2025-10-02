#!/bin/sh

alembic upgrade head

uvicorn --host 0.0.0.0 fast_zero.app:app