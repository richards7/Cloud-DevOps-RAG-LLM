# Microservices Architecture

## What it is
Microservices structure an application as a collection of small, independently
deployable services, each owning a specific business capability (e.g. "orders
service", "users service"), communicating over the network (usually REST/gRPC/message
queues) rather than in-process function calls.

## Microservices vs monolith
- **Monolith**: one codebase, one deployment unit. Simpler to develop and deploy
  initially, but harder to scale specific parts independently and riskier to deploy
  (any change requires redeploying the whole app).
- **Microservices**: independent services, independently deployable and scalable, but
  add operational complexity — network calls replace function calls, and you need
  service discovery, monitoring, and distributed tracing to keep visibility.

## Key patterns
- **API Gateway**: a single entry point that routes requests to the right service,
  often handling auth, rate limiting, and request aggregation.
- **Service discovery**: how services find each other's network location dynamically
  (e.g. Kubernetes' built-in DNS-based service discovery), since IPs change as
  containers restart/scale.
- **Database per service**: each microservice typically owns its own database, so
  services aren't coupled through shared tables — cross-service queries happen over
  APIs, not direct DB joins.
- **Circuit breaker**: stops calling a failing downstream service temporarily (instead
  of endlessly retrying) to prevent cascading failures across the system.
- **Event-driven communication**: services communicate asynchronously via a message
  queue/event bus (e.g. SNS/SQS, Kafka) instead of direct synchronous calls, improving
  resilience and decoupling.

## Containerization's role
Docker packages each microservice with its dependencies into a portable container;
Kubernetes then orchestrates running many of these containers reliably at scale —
this pairing is why microservices and containers are so closely associated in
practice.

## Trade-offs (a common interview discussion point)
Microservices aren't automatically "better" — they solve organizational scaling
(different teams owning different services) and independent-deployment problems, at
the cost of network latency, distributed debugging complexity, and operational
overhead. A monolith is often the right starting choice for a small team/early-stage
product.

## Common errors & fixes
- **Cascading failures**: one slow/failing service causes timeouts across the whole
  system — mitigate with circuit breakers, timeouts, and retries with backoff.
- **Data inconsistency across services**: without shared transactions, use patterns
  like the Saga pattern (a sequence of local transactions with compensating actions on
  failure) instead of expecting strict cross-service ACID guarantees.
- **Difficult debugging**: a single user request may touch many services — distributed
  tracing (e.g. OpenTelemetry) and correlation IDs in logs are essential to trace a
  request across service boundaries.
