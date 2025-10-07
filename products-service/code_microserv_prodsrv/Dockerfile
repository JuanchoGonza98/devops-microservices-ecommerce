# Etapa 1: Build
FROM gradle:8.7-jdk17-alpine AS build
WORKDIR /app
COPY . .
RUN gradle clean build -x test

# Etapa 2: Runtime
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
