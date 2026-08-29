# understand-repo

Analyse the target repository and produce a `repo_context` block conforming to `onboarding.schema.json`. Run this phase whenever `repo_context` is absent or any coverage flag is `false`.

## Methodology

**Structure before implementation.** Read config files, directory layout, and entry-point manifests before touching implementation files. The shape of the repo tells you more than any single source file.

**Evidence over inference.** Every claim in `summary` must be traceable to a file you read. Never infer a framework from a file name alone; open the file and confirm.

**Follow relationships.** Start at entry points and walk import/require/call chains outward. Stop when the chain reaches a third-party boundary or circles back.

**Representative evidence.** One clear example per concept is enough. Do not read every file in a hot directory; read the most representative one.

**Stop when sufficient.** Coverage is done when every flag in the checklist below is `true`, or you have a documented reason the area does not apply (mark `true` for N/A areas).

## Investigation order

1. Top-level files: `README`, `package.json` / `pyproject.toml` / `Cargo.toml`, `Makefile`, `docker-compose.yml`, `.env.example`.
2. Directory listing (one level deep) to establish regions.
3. Entry points: `src/index.*`, `main.*`, `app.*`, `server.*`, `cmd/`.
4. Architecture signals: `src/`, `lib/`, `packages/`, `modules/`, `services/`, monorepo workspace files.
5. Data layer: ORM config, migration files, schema files, seed scripts.
6. Frontend: component directories, router config, build config.
7. Infra: Dockerfile, CI config (`.github/workflows`, `Jenkinsfile`), terraform / CDK / pulumi.
8. Tests: test runner config, one representative test file per region.
9. Conventions: `.eslintrc`, `prettier.config`, `tsconfig`, `CONTRIBUTING.md`, commit lint config.
10. Hotspots: files changed most in recent git log (run `git log --oneline --name-only -50` if available).

## Coverage checklist

Mark each flag `true` when you have evidence. Mark `true` if the area does not apply to this repo (e.g. `frontend: true` for a pure API service, with a note in `summary`).

| Flag | Evidence required |
|---|---|
| `project` | Purpose, name, primary language, license |
| `entry_points` | How the app starts; what runs it |
| `architecture` | Layers, packages, or service boundaries |
| `runtime_flows` | At least one end-to-end request/job/event traced |
| `interfaces` | Public API surface: REST routes, GraphQL schema, CLI commands, or exported functions |
| `data` | Database/store type, schema location, migration strategy |
| `frontend` | UI framework, routing, state management (or N/A) |
| `backend` | Server framework, middleware chain, auth strategy (or N/A) |
| `infra` | How it is built, containerised, and deployed |
| `testing` | Test runner, coverage strategy, how to run tests |
| `workflow` | Dev setup steps, CI/CD pipeline, branching strategy |
| `conventions` | Code style, linting, naming rules, PR process |
| `hotspots` | Files with highest churn; complexity hot-spots |

## Output

Populate `repo_context` in `onboarding-session.json`:

```json
{
  "repo_context": {
    "generated_at": "<ISO-8601>",
    "source_path": "<absolute path>",
    "coverage": { "project": true, "entry_points": true, "..." : true },
    "summary": "<narrative>",
    "tech_tags": ["react", "postgres", "docker"]
  }
}
```

`tech_tags` must use the normalised lowercase identifiers below where they match. Add new tags as lowercase for anything not listed.

**Normalised tags:** `react`, `vue`, `angular`, `svelte`, `nextjs`, `remix`, `vite`, `webpack`, `typescript`, `javascript`, `python`, `go`, `rust`, `java`, `csharp`, `ruby`, `php`, `postgres`, `mysql`, `sqlite`, `mongodb`, `redis`, `dynamodb`, `prisma`, `drizzle`, `typeorm`, `graphql`, `rest`, `grpc`, `trpc`, `express`, `fastify`, `nestjs`, `django`, `fastapi`, `rails`, `docker`, `kubernetes`, `terraform`, `pulumi`, `aws`, `gcp`, `azure`, `github-actions`, `jest`, `vitest`, `pytest`, `playwright`, `cypress`.