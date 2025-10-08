# 🧩 Etapa 1: Build (compilación con Gradle)
FROM gradle:8.7-jdk17-alpine AS build
WORKDIR /app
COPY . .
RUN gradle clean build -x test

# 🧩 Etapa 2: Runtime (ejecución)
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8082
ENTRYPOINT ["java", "-jar", "app.jar"]
