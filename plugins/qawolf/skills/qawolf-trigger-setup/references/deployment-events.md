# Emitting deployment events

How a pipeline creates the GitHub or GitLab deployments a deployment trigger fires on. Reached from [Trigger Setup](../SKILL.md#choose-the-trigger-kind); many hosting providers, such as Vercel, create these events on their own, so check for that before adding anything.

## The environment name is the contract

The deployment's environment name is what QA Wolf matches against the workspace's environments, by alias or by slugified name. When nothing matches, QA Wolf creates a new environment under that name. That cuts both ways:

- A name that matches the intended QA Wolf environment lands the deploy exactly where the triggers look.
- A name that does not match silently creates a second environment the existing triggers do not target. A pipeline sending `prod-us` while the QA Wolf environment is named `production` produces runs in neither.

So settle the name deliberately: make the pipeline emit the QA Wolf environment's name, or add that name as the environment's alias. Per-pull-request preview names (`preview/pr-42` on GitHub, `review/pr-42` on GitLab) are the exception: each one is meant to create its own short-lived environment.

## Isolate previews per pull request

A preview deployment must be isolated per pull request in two independent ways, and a pipeline missing either is a mistake to correct, not a preference to accept, because neither failure announces itself:

- **The environment name needs a per-PR discriminator:** `preview/pr-42` on GitHub, `review/pr-42` on GitLab, never a bare `preview`. A single shared preview environment means every pull request's deployment overwrites the same environment's deploy target, so a run triggered by one pull request can execute against another's build, concurrent pull requests collide on environment state, and when the environment is transient, closing any one pull request terminates the environment every other open one is still using.
- **The deploy target URL needs a discriminator too**, and this failure is silent. With per-PR names but a static URL, the environment is isolated, the trigger matches, and the run executes against whatever was deployed last, not the pull request under test. The result is a green run for code that was never exercised. Any unique-per-deployment discriminator works: the pull request number, the commit sha, the branch slug.

## Long-lived versus transient

A deployment must say whether its environment is permanent or per-branch, because that decides what kind of environment QA Wolf creates for an unmatched name:

- On GitHub, set `transient_environment: true` for a preview or pull-request deploy, and `false` for a long-lived environment such as staging. Omitting it marks every deploy long-lived, so previews without it pile up as permanent environments.
- On GitLab there is no transient flag, so the name itself decides: a preview environment's name must start with `review/`, GitLab's review-apps prefix, or QA Wolf treats each created environment as long-lived and never tears it down. This is a naming requirement, not a style choice: a GitLab preview named `preview/pr-42` piles up permanently.

Only a deployment that reports success evaluates triggers. The deploy URL (`environment_url` on GitHub, the environment's `url` on GitLab) becomes the deployment's deploy target, which `deployTargetPattern` matches and a created environment takes as its URL.

## GitHub

The workflow needs `permissions: deployments: write`. A long-lived deploy creates the deployment and reports success once the deploy finishes:

```yaml
- uses: actions/github-script@v7
  with:
    script: |
      const deployment = await github.rest.repos.createDeployment({
        ...context.repo,
        ref: context.sha,
        environment: "staging",
        transient_environment: false,
        auto_merge: false,
        required_contexts: [],
      });
      await github.rest.repos.createDeploymentStatus({
        ...context.repo,
        deployment_id: deployment.data.id,
        state: "success",
        environment_url: "https://staging.example.com",
      });
```

`auto_merge: false` and `required_contexts: []` keep the API from refusing or deferring the deployment behind branch checks.

A preview deploy differs in three fields: it runs on `pull_request`, deploys `ref: pullRequest.head.sha` to an environment named for the pull request, and marks it transient:

```javascript
environment: `preview/pr-${pullRequest.number}`,
transient_environment: true,
```

## GitLab

A job with the `environment:` keyword creates the deployment on its own; a separate API call is unnecessary. The deployment webhook fires when the job succeeds:

```yaml
deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./deploy.sh
```

A review app names its environment per branch, which the `review/` prefix marks transient:

```yaml
environment:
  name: review/$CI_COMMIT_REF_SLUG
  url: https://$CI_COMMIT_REF_SLUG.example.com
```

## Verify

Only a real deploy proves the wiring: the event must leave the pipeline, reach QA Wolf through the connected integration, and match the trigger. After the change lands, [Trigger Setup](../SKILL.md#create-a-deployment-trigger) says how to confirm the run appeared and where to go when it did not.
