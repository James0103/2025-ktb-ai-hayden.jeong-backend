#!/bin/bash

USERNAME="james0103"
VERSION=$(date +%Y%m%d_%H%M%S)  # 2025-01-15_143022

# Backend
cd backend
docker build -t ghcr.io/$USERNAME/relay-story-backend:$VERSION .
docker tag ghcr.io/$USERNAME/relay-story-backend:$VERSION ghcr.io/$USERNAME/relay-story-backend:latest
docker push ghcr.io/$USERNAME/relay-story-backend:$VERSION
docker push ghcr.io/$USERNAME/relay-story-backend:latest
cd ..

# Frontend
cd frontend
docker build -t ghcr.io/$USERNAME/relay-story-frontend:$VERSION .
docker tag ghcr.io/$USERNAME/relay-story-frontend:$VERSION ghcr.io/$USERNAME/relay-story-frontend:latest
docker push ghcr.io/$USERNAME/relay-story-frontend:$VERSION
docker push ghcr.io/$USERNAME/relay-story-frontend:latest
cd ..

echo "✅ 배포 완료! (버전: $VERSION)"