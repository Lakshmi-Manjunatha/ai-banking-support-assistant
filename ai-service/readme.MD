# AI Service

The AI/RAG backend for the [AI Banking Support Assistant](../README.md). This service answers natural-language banking questions using retrieved policy documents and Gemini. It currently uses **LangChain** for document loading, chunking, embeddings integration, and PostgreSQL vector retrieval.

This is one of three application services in the project. It currently answers from policy documents; it does not call the customer or transaction APIs for live account information.

## Architecture and request flow

```mermaid
flowchart LR
    Client[API client] -->|Question and Bearer token| API[FastAPI]
    API --> Auth[JWT validation and role check]
    Auth -->|Signing keys via JWKS| Keycloak[Keycloak]
    Auth --> Retrieval[LangChain retrieval]
    Retrieval -->|Query embedding| Embeddings[Gemini embeddings]
    Retrieval -->|Similarity search| DB[(PostgreSQL and pgvector)]
    Retrieval --> Context[Filter chunks and build prompt]
    Context --> Gemini[Gemini answer generation]
    Gemini --> Answer[JSON answer to client]
    Files[TXT, PDF, DOCX policies] --> Ingestion[Load and chunk documents]
    Ingestion --> Embeddings
    Embeddings -->|Document vectors via ingestion| DB
```

### Document ingestion

1. Load `.txt`, `.pdf`, and `.docx` files from `BANK_POLICY_FILES_PATH`.
2. Attach document ID and version metadata.
3. Split text with `RecursiveCharacterTextSplitter` using configured chunk size and overlap.
4. Assign chunk indexes and deterministic UUIDs from document ID, version, and chunk index.
5. Generate embeddings and store chunks, metadata, and vectors through `PGVectorStore`.

Ingestion is a separate command or Kubernetes Job; it does not run automatically for each question.

### Question answering

1. Accept `POST /api/v1/ask` and validate the question.
2. Verify the Bearer token's RS256 signature, expiry, issuer, and audience through Keycloak JWKS.
3. Require `rag:ask` under `resource_access.banking-ai-api.roles`.
4. Embed the question and search PostgreSQL/pgvector for candidate policy chunks.
5. Filter results by maximum distance and cap the number of returned documents.
6. Combine the retrieved text and question in a prompt instructing Gemini to use only the provided context and acknowledge insufficient information.
7. Return the generated text in an `answer` field. Context-only answering is prompt guidance, rather than a separate deterministic answer check.

## Technology stack

| Area | Technology |
| --- | --- |
| Runtime and API | Python 3.12 in Docker, FastAPI, Uvicorn, Pydantic |
| RAG | LangChain, community document loaders, recursive text splitting, `langchain-google-genai`, `langchain-postgres` |
| AI | Gemini embeddings and Google Gen AI SDK for answer generation |
| Storage | PostgreSQL, pgvector, SQLAlchemy, Psycopg |
| Document parsing | `pypdf`, `docx2txt`, text loaders |
| Authentication | Keycloak-issued JWTs, PyJWT with cryptographic support, RS256, JWKS, role checks |
| Configuration and logging | `python-dotenv`, environment variables, Python console/file logging |
| Tests | pytest, FastAPI TestClient |
| Delivery | Docker, GitHub Actions, Docker Hub, self-hosted Windows runner, kubectl, Kustomize |

Alembic is listed in `requirements.txt`; the active vector-store module initializes its table if it does not exist. Earlier manual RAG code remains in `app/rag` and `app/db`, but the active answer path uses `app/lagchain_rag` (spelled this way in the repository).

## Local setup

Prerequisites: Python 3.12, a PostgreSQL database with pgvector available, Gemini API access, and a configured Keycloak realm/client that issues tokens for this API.

From the repository root, use PowerShell:

```powershell
cd ai-service
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Populate `.env` before ingestion or starting the application:

| Variable | Purpose / example |
| --- | --- |
| `GEMINI_API_KEY` | Gemini API credential |
| `GEMINI_LLM_MODEL_NAME` | Available Gemini generation model; Kubernetes configuration currently uses `gemini-2.5-flash` |
| `GEMINI_EMBEDDING_MODEL_NAME` | Available embedding model; Kubernetes configuration currently uses `gemini-embedding-2` |
| `DATABASE_URL` | Full SQLAlchemy connection URL, e.g. `postgresql+psycopg://USER:PASSWORD@localhost:5432/POLICY_DB` |
| `DOC_CHUNK_TABLE_NAME` | Vector table, e.g. `bank_policy_langchain_doc_chunks` |
| `BANK_POLICY_FILES_PATH` | Directory of policy documents, e.g. `../test_documents` |
| `EMBEDDING_DIMENSION` | Vector dimension, currently `768`; must match stored vectors |
| `CHUNK_SIZE`, `CHUNK_OVERLAP` | Text splitting settings, currently `500` and `100` |
| `RETRIEVER_DOCUMENT_FETCH_LIMIT` | Candidate count, currently `20` |
| `RETRIEVER_DOCUMENT_MAX_DISTANCE` | Maximum accepted distance, currently `0.5` |
| `NUMBER_OF_DOC_RETURN` | Maximum selected chunks, currently `3` |
| `KEYCLOAK_ISSUER` | Exact token issuer, e.g. `http://localhost:8180/realms/banking` |
| `KEYCLOAK_AUDIENCE` | Expected audience, normally `banking-ai-api` |
| `JWKS_URL_SUFFIX` | Set to `/protocol/openid-connect/certs`; the current validator evaluates this configuration even when an explicit JWKS URL is supplied |
| `KEYCLOAK_JWKS_URL` | Reachable signing-key endpoint, e.g. `http://localhost:8180/realms/banking/protocol/openid-connect/certs` |
| `LOG_LEVEL`, `LOG_TO_FILE` | Logging level and optional file output; see `.env.example` for rotation settings |

Use `BANK_POLICY_FILES_PATH` (plural) for the active LangChain loader. The older singular `BANK_POLICY_FILE_PATH` entry belongs to the earlier flow. The application reads the full `DATABASE_URL`; separate host/port/name variables alone do not replace it.

The database must exist, and the connecting user must have the permissions required to initialize the vector store. Ingest policies, then start the API:

```powershell
.\.venv\Scripts\python.exe -m app.lagchain_rag.ingest
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`. Startup imports initialize model and database dependencies, so configure them even when only checking the health endpoint.

## API

| Method | Endpoint | Authentication |
| --- | --- | --- |
| GET | `/api/v1/health` | Public |
| POST | `/api/v1/ask` | Bearer JWT with `rag:ask` role |

Questions are trimmed and must contain 3-500 characters.

```http
POST /api/v1/ask
Authorization: Bearer <access-token>
Content-Type: application/json

{"question": "Why might my transaction be declined?"}
```

Successful response shape:

```json
{"answer": "Generated answer based on retrieved banking policy context."}
```

Errors include `401` for missing/invalid tokens, `403` for missing permissions, `422` for invalid input, `503` when signing keys cannot be obtained, and `500` for unhandled failures. Error responses use `success: false` and an `error` field; validation errors also include `details`.

## Tests

From `ai-service`, with the configured environment and database available:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The tests cover health, authentication/authorization, question validation, and error handling. Request tests mock token validation and answer generation, but imports still initialize configured dependencies. The CI workflow currently builds the Docker image without running these tests.

## Docker

From `ai-service`:

```shell
docker build -t ai-banking-service:local .
docker run --rm --env-file .env -p 8000:8000 ai-banking-service:local
```

Use database and JWKS addresses reachable from the container. The image copies application code, not local policy documents; ingestion needs a separately mounted directory and an appropriate `BANK_POLICY_FILES_PATH`.

## CI/CD

```mermaid
flowchart LR
    PR[Pull request to main] --> CI[Ubuntu runner - Docker build validation]
    CI -->|Same-repository PR| Hub[Publish tagged image to Docker Hub]
    Hub --> Manual[Manual CD run with image_tag]
    Manual --> Runner[Self-hosted Windows X64 runner]
    Runner --> Configure[Verify cluster and configure Kustomize image]
    Configure --> Apply[Apply preview overlay]
    Apply --> Rollout[Wait for rollout - 120 seconds]
    Rollout --> Verify[List preview resources]
```

### CI: build and publish

The [AI Service PR CI workflow](../.github/workflows/ai-service-ci.yaml) runs when pull requests targeting `main` are opened, updated, or reopened. It builds the Docker image on `ubuntu-latest`. Same-repository PRs also publish to Docker Hub using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets:

```text
<DOCKERHUB_USERNAME>/ai-banking-service:pr-<PR_NUMBER>-<FULL_HEAD_SHA>
```

Fork PRs receive build validation only. CI does not deploy the image.

### CD: manual preview deployment

The [AI Service CD workflow](../.github/workflows/ai-service-cd.yaml) is triggered manually through `workflow_dispatch` with the required `image_tag` input. It uses an existing published image, without rebuilding it.

1. Check out the selected ref on a runner labelled `self-hosted`, `Windows`, `X64`.
2. Verify the runner's current Kubernetes context and list cluster nodes.
3. Replace image placeholders in the [preview overlay](../k8s/overlays/preview/kustomization.yaml) using `DOCKERHUB_USERNAME` and `image_tag`.
4. Render the overlay, then run `kubectl apply -k k8s/overlays/preview` from the repository root.
5. Wait for `ai-service-deployment` in `ai-service-preview` with a `120s` timeout, then list deployments, pods, and services. Failed kubectl commands fail the job.

Before running CD, provide:

- An online Windows X64 runner with PowerShell, kubectl, and cluster access through its kubeconfig.
- The `ai-service-preview` namespace and permission to apply resources there and inspect nodes.
- The `DOCKERHUB_USERNAME` repository secret and a published image tag. Private images require separately configured registry pull credentials.
- A `banking-ai-secret` Secret in the preview namespace containing required credentials and database connection configuration.
- Reachable PostgreSQL/pgvector and Keycloak with matching configuration, plus separately ingested policy data.

The preview overlay applies only the AI Deployment, ClusterIP Service, and ConfigMap. It does not create the namespace, Secrets, PostgreSQL, document volumes, or ingestion Job. The Deployment uses `/api/v1/health` for startup, readiness, and liveness probes.

To deploy, open GitHub **Actions > AI Service CD > Run workflow**, choose the repository ref, and enter the existing tag (for example, `pr-42-<full-head-sha>`) without the image repository name.

For local access after rollout, run from a machine with cluster access:

```shell
kubectl port-forward service/ai-service-service 8000:8000 -n ai-service-preview
```

Check `http://localhost:8000/api/v1/health` and `http://localhost:8000/docs`. An answer check also requires a valid token and ingested documents. CD currently verifies rollout and lists resources; it does not perform an API smoke test, automatically roll back failures, or promote to production. Redeploy an earlier image by running CD again with its existing tag.

See the [project README](../README.md) for the architecture of all three services.
