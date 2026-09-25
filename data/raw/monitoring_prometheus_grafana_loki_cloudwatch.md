# Monitoring — Prometheus, Grafana, Loki, CloudWatch

## Why monitoring matters (the DevOps angle)
Monitoring answers "is the system healthy right now, and why isn't it?" — the
difference between reacting to a customer complaint and catching an issue before it
becomes one. Three pillars: **metrics** (numbers over time), **logs** (event records),
**traces** (a request's path across services).

## Prometheus
An open-source metrics collection and alerting system. Prometheus **pulls** (scrapes)
metrics from targets at regular intervals, rather than targets pushing to it — a key
architectural difference from many older monitoring tools.

- **Exporters**: small processes that expose a service's metrics in Prometheus format
  (e.g. `node_exporter` for host-level metrics, or an app exposing a `/metrics`
  endpoint directly).
- **PromQL**: Prometheus's query language.
```promql
# Current value of a metric
up

# Rate of HTTP requests over the last 5 minutes
rate(http_requests_total[5m])

# Alert-style query: error rate above 5%
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
```
- **Alertmanager**: a separate component that receives alerts from Prometheus (based
  on rules) and routes them to Slack/email/PagerDuty, handling deduplication and
  grouping.

## Grafana
A visualization layer that queries Prometheus (and many other data sources —
CloudWatch, Loki, SQL databases) to build dashboards. Grafana doesn't store metrics
itself; it visualizes data from a connected source.

- Dashboards are made of **panels** (graphs, gauges, tables), each backed by a query.
- Alerting can also live in Grafana itself, as an alternative/complement to
  Prometheus's Alertmanager.

## Loki
A log aggregation system built by the Grafana team, designed to be cheap and simple by
indexing only metadata (labels), not the full log text — unlike Elasticsearch, which
indexes everything. Queried with **LogQL**, syntactically similar to PromQL.
```logql
{app="myapp", env="production"} |= "ERROR"
```
This means: logs from `myapp` in `production`, containing the text "ERROR".

## CloudWatch (AWS-native)
AWS's built-in monitoring service — collects metrics from AWS resources
automatically (EC2 CPU usage, Lambda invocations, etc.), and can also receive custom
application metrics and logs.
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0abcd1234 \
  --start-time 2026-01-01T00:00:00Z --end-time 2026-01-02T00:00:00Z \
  --period 3600 --statistics Average

aws logs tail /aws/lambda/my-function --follow
```
- **CloudWatch Alarms**: trigger actions (e.g. auto-scaling, SNS notification) when a
  metric crosses a threshold.
- **CloudWatch Logs Insights**: a query language for searching/analyzing log data
  directly in CloudWatch.

## Choosing between them (a common practical question)
- Fully on AWS, want the simplest setup → **CloudWatch** (native, no extra
  infrastructure to run).
- Multi-cloud, Kubernetes-heavy, or want full control/cost efficiency at scale →
  **Prometheus + Grafana** (the de facto standard in cloud-native/Kubernetes
  environments) with **Loki** for logs, keeping the whole stack open-source.
- Most real-world setups mix both — e.g. CloudWatch for AWS-native metrics, Prometheus
  for Kubernetes workloads, Grafana as a single pane of glass over everything.

## Common errors & fixes
- **Prometheus target shows "down"**: the exporter/app isn't exposing `/metrics`, or a
  firewall/security group blocks the scrape — check `curl <target>:<port>/metrics`
  directly from the Prometheus host.
- **Grafana panel shows "No data"**: check the data source connection and that the
  time range selected actually overlaps with when data exists.
- **Alert fires but no notification received**: check Alertmanager's routing
  config/receiver setup, or (in Grafana-native alerting) the contact point
  configuration — a misconfigured route silently drops alerts.
- **CloudWatch Logs Insights query too slow/expensive**: narrow the time range and log
  group scope first; broad queries across huge log groups scan a lot of data and cost
  more.
- **Loki "too many outstanding requests"**: usually querying too broad a label set or
  too wide a time range at once — narrow the label selectors.
