# Exercícios Docker

## Exercício 1

### a)

```sh
docker run -d --name conteiner-exer1a -p 3001:3011 imagem-exemplo1:1.0.0
curl http://localhost:3001
```

### b)

```sh
docker run -d --name conteiner-exer1b -p 3002:3011 imagem-exemplo1:1.0.0
curl http://localhost:3002
```

## Exercício 2

### a)

```sh
docker ps -a
```

### b)

```sh
docker inspect container-exer1a
```

### c)

```sh
docker stop container-exer1a container-exer1b
```

### d)

```sh
docker rm container-exer1a container-exer1b
```

## Exercício 3

### a)

```sh
docker run -d --name container-exer3 -p 3003:3011 imagem-exemplo1:1.1.0
```

## Exercício 4

```sh
docker build -t imagem-exemplo2:1.0.0 .
docker run -d --name container-exer4 -p 3004:3012 imagem-exemplo2:1.0.0
curl http://localhost:3004
```
