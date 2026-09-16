# Production readiness checklist

- [ ] Secrets are stored in a secure secret manager, not committed to source control
- [ ] `.env` contains no production values
- [ ] API keys are configured for the target environment
- [ ] CORS allowlist is restricted to production domains
- [ ] Frontend build passes in CI
- [ ] Backend tests pass in CI
- [ ] Health endpoints are reachable
- [ ] `/metrics` is enabled and monitored
- [ ] Production Docker config is used for deploys
- [ ] Local dev override is not used in production
- [ ] Rate limiting is enabled
- [ ] Authentication is enforced on protected APIs
- [ ] Rollback plan is documented
- [ ] Monitoring and alerting are configured
- [ ] Deployment validation has been performed in a staging environment

## Post-deploy smoke tests
- [ ] `/health` returns `200`
- [ ] `/health/live` returns `200`
- [ ] `/health/ready` returns `200`
- [ ] `/metrics` returns metrics output
- [ ] Protected route returns `401` without API key
- [ ] Protected route accepts valid API key
- [ ] Frontend loads successfully against production backend
