#!/usr/bin/env bash

cd /app
PYTHONUNBUFFERED=1 sage kernel_searcher.sage 2>&1
