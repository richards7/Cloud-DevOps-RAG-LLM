# Jenkins

Jenkins is an open-source automation server used to build CI/CD pipelines — compiling,
testing, and deploying code automatically on triggers like a Git push.

## Core concepts
- **Job/Project**: a single automated task (e.g. "build-and-test").
- **Pipeline**: a job defined as code (a `Jenkinsfile`), usually checked into the repo
  itself — preferred over manual UI-configured jobs for repeatability and version control.
- **Agent/Node**: the machine (or container) that actually runs the pipeline steps.
- **Plugin**: Jenkins' extensibility model — plugins add support for Git, Docker,
  Slack notifications, credentials management, and more.

## Declarative Jenkinsfile example
```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps { sh 'docker build -t $IMAGE_NAME .' }
        }
        stage('Test') {
            steps { sh 'pytest tests/' }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps { sh 'docker push myregistry/$IMAGE_NAME' }
        }
    }

    post {
        failure {
            echo 'Pipeline failed — check logs.'
        }
    }
}
```

## Triggers
- **Poll SCM**: Jenkins periodically checks the repo for changes.
- **Webhooks**: the Git provider (GitHub/GitLab) notifies Jenkins immediately on push —
  preferred, since it's instant and doesn't waste resources polling.

## Credentials management
Jenkins has a built-in Credentials store so secrets (API keys, SSH keys, tokens) aren't
hardcoded in the Jenkinsfile — referenced instead via `credentials('my-cred-id')`.

## Common errors & fixes
- **"Permission denied" running Docker inside a Jenkins agent**: the Jenkins user
  usually needs to be in the `docker` group on the host:
  `sudo usermod -aG docker jenkins` then restart Jenkins.
- **Pipeline hangs on "Waiting for next available executor"**: no agent matches the
  required `agent` label, or all executors are busy — check node configuration.
- **Webhook not triggering builds**: check the webhook URL/secret on the Git provider
  side, and confirm Jenkins is reachable from the internet (or the Git provider) if
  self-hosted, e.g. via a public IP/reverse proxy and correct firewall rules.
- **"No such property" in Jenkinsfile**: usually a Groovy/Declarative syntax issue —
  the Jenkins "Replay" or "Pipeline Syntax" tool in the UI helps validate steps.
