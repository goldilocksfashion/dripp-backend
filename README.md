# Backend Infrastructure Services

Welcome to **Dripp.ai**! This document provides an overview of the backend infrastructure services structured within specific bounded contexts. Each bounded context encapsulates a set of capabilities and data that are coherent within a specific domain boundary.

## Table of Contents

- [Introduction](#introduction)
- [Bounded Contexts](#bounded-contexts)
	- [Content Management](#content-management)
	- [Dream Journal and Aspiration Management](#dream-journal-and-aspiration-management)
	- [Virtual Try-On (VTO) Service](#virtual-try-on-vto-service)
	- [Social Network and Interaction](#social-network-and-interaction)
	- [Marketplace](#marketplace)
	- [Event and Tag Management](#event-and-tag-management)
- [Event-Driven Architecture](#event-driven-architecture)
	- [Kafka Backbone](#kafka-backbone)
- [Getting Started](#getting-started)
- [Architecture Diagram](#architecture-diagram)
- [Development and Contributions](#development-and-contributions)
- [Contact Information](#contact-information)

## Introduction

This project is designed to support a scalable, microservices-oriented architecture where each service is loosely coupled but coordinated through events and shared data models. The services are organized into bounded contexts, each representing a distinct functional area within our application.

## Bounded Contexts

### Content Management

- **Purpose**: Manages all content-related functionalities including storage, retrieval, and content delivery.
- **Key Components**: Content database, caching mechanisms, content delivery network integration.
- **Technologies Used**: [Technologies, e.g., MongoDB, Redis, AWS S3]

### Dream Journal and Aspiration Management

- **Purpose**: Facilitates the management of user aspirations and dream journals, offering features to record and track user goals related to products or services.
- **Key Components**: User profile management, journal entry datastore.
- **Technologies Used**: [Technologies, e.g., PostgreSQL, Node.js]

### Virtual Try-On (VTO) Service

- **Purpose**: Provides virtual try-on capabilities for apparel and accessories using advanced image processing and rendering technologies.
- **Key Components**: Image processing service, 3D modeling tools.
- **Technologies Used**: [Technologies, e.g., OpenCV, Three.js]

### Social Network and Interaction

- **Purpose**: Supports social interactions within the platform such as comments, likes, and sharing.
- **Key Components**: Interaction service, notification system.
- **Technologies Used**: [Technologies, e.g., RabbitMQ, Socket.IO]

### Marketplace

- **Purpose**: Handles all e-commerce transactions, product listings, and order management.
- **Key Components**: Product catalog, payment gateway integration, order processing workflow.
- **Technologies Used**: [Technologies, e.g., Stripe, Elasticsearch]

### Event and Tag Management

- **Purpose**: Manages event logging, processing, and tagging to enhance system observability and event-driven interactions across services.
- **Key Components**: Kafka event streams, event database.
- **Technologies Used**: [Technologies, e.g., Apache Kafka, MongoDB]

## Event-Driven Architecture

The event-driven architecture is designed to facilitate seamless data flow between microservices. This allows for high scalability, fault tolerance, and responsiveness in real time.

### Kafka Backbone

Apache Kafka serves as the backbone of the event-driven architecture, providing reliable and fault-tolerant streaming services. Key features include:

- **Event Producers**: Microservices produce events that are streamed to Kafka topics.
- **Event Consumers**: Other microservices consume the relevant topics, process the data, and trigger appropriate downstream actions.
- **Schema Registry**: Ensures consistent event schemas across all producers and consumers.
- **Monitoring**: Prometheus and Grafana are used for monitoring Kafka metrics.

## Getting Started

To set up the project locally, follow these steps:
1. Clone the repository: `git clone [Repository URL]`
2. Install dependencies: `cd [Repository Name] && npm install`
3. Configure environment variables: Copy `.env.example` to `.env` and update values.
4. Start the development server: `npm start`

## Architecture Diagram

Confluence gliffy diagrams here

## Development and Contributions

Contributions to the project are welcome! Please refer to the `CONTRIBUTING.md` for guidelines on how to make contributions.

## Contact Information

For any queries or further information, please contact:
- av@goldilocksfashion.com
- heejee.jo@goldilocksfashion.com
- eda.zhang@goldilocksfashion.com
