# Production Release Notes

## Summary
This release hardens the RAG application for production use by improving security, deployment readiness, and operational observability.

## Highlights
- Fixed frontend TypeScript/Vite build issues
- Installed and validated the backend Python dev/test stack
- Removed committed secret values from local config
- Restricted CORS to explicit production origins
- Added API key enforcement and in-memory rate limiting
- Added health, readiness, and metrics endpoints
- Split development and production Docker configuration
- Added CI checks for frontend build and backend tests
- Added startup and monitoring safeguards for runtime health

## Security updates
- Secret values are no longer stored in committed environment files
- API key enforcement is enabled for protected routes
- CORS is restricted to configured allowlisted origins
- Rate limiting is applied to non-public endpoints

## Monitoring and health
- Added `/health`
- Added `/health/live`
- Added `/health/ready`
- Added `/metrics`

## Deployment changes
- Production Docker settings are separated from local development settings
- CI now enforces build + test validation before deployment
- Frontend production build is validated before release

## Verification
- Backend tests: passed
- Frontend build: passed

### Test evidence
- `PYTHONPATH=. pytest -q` → `4 passed in 48.99s`
- `npm run build` in the frontend → Vite production build completed successfully

## Notes
- Upstream dependency deprecation warnings remain in the stack but do not block deployment.
- These warnings should be tracked as a future modernization task.

## Recommended next deployment steps
1. Set real values for `GEMINI_API_KEY`, `API_KEYS`, and `CORS_ALLOWED_ORIGINS`
2. Use a production secret manager instead of `.env`
3. Deploy via the production Docker configuration
4. Validate `/health`, `/health/live`, `/health/ready`, and `/metrics`
5. Confirm API access with valid and invalid keys
