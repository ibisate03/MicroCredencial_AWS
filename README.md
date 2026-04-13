🛒 Sistema Serverless de Gestión de Pedidos en AWS
📌 Descripción general

Este proyecto implementa un sistema de gestión de pedidos serverless utilizando servicios de AWS.

Permite a los usuarios:

Crear pedidos desde una interfaz web
Almacenarlos en base de datos
Procesarlos de forma asíncrona
Recibir un correo de confirmación

La arquitectura sigue un enfoque orientado a eventos y basado en microservicios.

🏗️ Arquitectura

El sistema está compuesto por varios servicios conectados en pipeline:

Frontend (S3)
     ↓
API Gateway
     ↓
Lambda (create-order)
     ↓
DynamoDB + EventBridge
     ↓
SQS
     ↓
Lambda (process-order)
     ↓
DynamoDB (update) + SNS (email)
⚙️ Componentes / Microservicios
1. Frontend (S3)
Aplicación web estática alojada en Amazon S3
Permite:
Crear pedidos
Consultar estado de pedidos
Se comunica con API Gateway mediante HTTP
2. API Gateway
Expone endpoints HTTP:
POST /orders → crear pedido
GET /orders/{id} → consultar pedido
Encargado del enrutado hacia las Lambdas
Configurado con CORS
3. Lambda: create-order
Recibe peticiones desde API Gateway
Genera un ID único para el pedido
Guarda el pedido en DynamoDB con estado:
PENDING
Publica un evento en EventBridge
4. DynamoDB (tabla de pedidos)
Almacena todos los pedidos
Atributos principales:
Id
customerEmail
product
quantity
status
5. EventBridge
Captura eventos del tipo:
OrderCreated
Los redirige a SQS
6. SQS (cola de procesamiento)
Cola de mensajes para desacoplar el sistema
Recibe los eventos de pedidos creados
7. Lambda: process-order
Se activa al recibir mensajes de SQS
Actualiza el estado del pedido a:
PROCESSED
Envía una notificación mediante SNS
8. SNS (notificaciones)
Envía correos electrónicos al usuario
Incluye:
ID del pedido
Producto
Estado del pedido
🔄 Flujo de funcionamiento
El usuario crea un pedido desde el frontend
API Gateway envía la petición a create-order
El pedido se guarda en DynamoDB (PENDING)
Se genera un evento en EventBridge
EventBridge envía el evento a SQS
SQS activa la Lambda process-order
El pedido se actualiza a PROCESSED
SNS envía un correo de confirmación
🧪 Cómo usar la aplicación
Acceder al frontend (URL de S3)
Crear un pedido introduciendo:
Email
Producto
Cantidad
Copiar el orderId generado
Consultar el estado del pedido
Recibir confirmación por email
🧠 Características principales
Arquitectura serverless
Sistema asíncrono y desacoplado
Uso de eventos (EventBridge)
Escalabilidad automática
Separación clara de responsabilidades
⚠️ Notas
Es necesario confirmar la suscripción al email en SNS
Puede haber un pequeño retraso en el procesamiento (arquitectura asíncrona)
CORS debe estar habilitado en API Gateway para el frontend
🚀 Tecnologías utilizadas
AWS Lambda
Amazon API Gateway
Amazon DynamoDB
Amazon EventBridge
Amazon SQS
Amazon SNS
Amazon S3
