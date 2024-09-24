# Ejercicio práctico para Data Engineer Replication/Extraction en Deacero.

La estructura de carpetas del repositorio simula 3 servidores de Microsoft SQL Server uno con datos centrales y otros con datos por sucursal:

```
data
├── central
│   ├── CatLineasAereas.csv
├── sucursal1
│   ├── Pasajeros.csv
│   ├── Vuelos.csv
├── sucursal2
│   ├── Pasajeros.csv
│   ├── Vuelos.csv
```
## Objetivo

El requerimiento funcional consiste en centralizar y replicar la información en el datawareohuse de Bigquery.

Para esto debe realizar las implementaciones técnicas que considere necesarias para la replicación de datos con CDC y SQL Replicate hacia Bigquery.

## Información clave

- Deben respetarse las tecnologías de CDC y SQL Replicate.
- Es importante generar un diagrama de arquitectura sobre la implementación.
- La actualización de datos debe buscar la menor latencia posible segun la tecnología que se implemente o proponga.
- Debe buscarse una implementación lo mas cercana al codigo posible.
- Tienes alguna propuesta o hallazgos respecto a garantizar la calidad/integridad de la replicacón?

## Entrega del Ejercicio

- Debe realizar un fork de este repositorio para desarrollar y entregar su trabajo o tambien puede subir su proyecto a un repositorio de GitHub y compartir el enlace en un correo dirigido a jguerrero@deacero.com.
- Asegúrese de que el repositorio incluya:
    - Todos los recursos usados o generados para la solucion de los ejercicios.
    - Documentación que explique el proceso seguido y las decisiones tomadas.
    - Instrucciones claras sobre cómo configurar y ejecutar el proyecto y sus artefactos.

Suerte a todos!!! :metal: :nerd_face: :computer:
