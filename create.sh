docker build -f Dockerfile . -t pgstream
docker create --name pgstream --ip localhost -p 8050:5432 -e POSTGRES_USER=foo -e POSTGRES_PASSWORD=bar -e POSTGRES_DB=pgstream -t pgstream
docker start pgstream