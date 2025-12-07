# Frontend Dockerfile
FROM node:20-alpine AS build

WORKDIR /app

# package.json, package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci --verbose

# 소스 복사
COPY . .

# 빌드 (에러 시 로그 출력)
RUN npm run build 2>&1 || (cat /app/node_modules/.vite/package.json 2>/dev/null && npm run build)

# 프로덕션 이미지
FROM node:20-alpine

WORKDIR /app

# serve 설치 (정적 파일 서빙)
RUN npm install -g serve

# 빌드된 파일 복사
COPY --from=build /app/dist ./dist

# 포트 3000 노출
EXPOSE 3000

# 애플리케이션 실행
CMD ["serve", "-s", "dist", "-l", "3000"]
