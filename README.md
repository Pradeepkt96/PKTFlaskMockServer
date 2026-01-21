# PKTFlaskMockServer
Mock server to run flask python code on docker with 3 containers

## Setup

docker-compose up -d --build mock-server
docker ps

## Test

curl.exe "http://localhost:5000/api/customers?page=1&limit=100"
curl.exe -X POST http://localhost:8000/api/ingest
curl.exe "http://localhost:8000/api/customers?page=1&limit=100"

## Hard Reset

docker-compose down -v
docker-compose up -d --build
curl.exe -X POST http://localhost:8000/api/ingest
