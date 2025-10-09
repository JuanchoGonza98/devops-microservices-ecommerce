# Imagen base ligera con Java 17
FROM openjdk:17-jdk-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el .jar generado por Gradle o Maven al contenedor
# Ajusta el nombre según el que se genere en build/libs/
COPY build/libs/payment-service-0.0.1-SNAPSHOT.jar app.jar

# Exponer el puerto donde escucha Spring Boot
EXPOSE 8082

# Comando que arranca la aplicación
ENTRYPOINT ["java", "-jar", "app.jar"]
