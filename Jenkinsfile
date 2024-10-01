pipeline {
    agent {
        kubernetes {
            label 'kaniko-agent'
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    agent: kaniko
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    imagePullPolicy: Always
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  volumes:
  - name: docker-config
    secret:
      secretName: docker-config
"""
        }
    }
    environment {
        REGISTRY = 'docker.io/vivektech'
        VOTE_IMAGE = "${REGISTRY}/vote"
        RESULT_IMAGE = "${REGISTRY}/result"
        DOCKER_CONFIG = '/kaniko/.docker/'
        GIT_URL = 'https://github.com/vivek-infra-automation/example-voting-app.git'
        COMMIT_ID = ''
        BRANCH = "${params.Build_Identity}"
        GITHUB_CREDENTIALS_ID = ''
        APPLICATION = "${params.Delivery}"
    }
    parameters {
        string(
            description: 'Branch name or commit ID to build',
            name: 'Build_Identity',
            defaultValue: 'main',
            trim: true
        )
        choice(
            choices: ['vote', 'result'],
            description: 'Application to Build and Deploy',
            name: 'Delivery'
        )
    }
    stages {
        stage('Checkout') {
            steps {
                script {
                    git url: GIT_URL, branch: BRANCH
                    COMMIT_ID = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                }
            }
        }

        stage('Build Application') {
            steps {
                container('kaniko') {
                    script {
                        def image = ""
                        if (APPLICATION == 'vote') {
                            image = "${VOTE_IMAGE}:${COMMIT_ID}"
                            sh """
                            /kaniko/executor \
                                --dockerfile vote/Dockerfile \
                                --context ${env.WORKSPACE}/vote \
                                --destination ${image}
                            """
                        } else if (APPLICATION == 'result') {
                            image = "${RESULT_IMAGE}:${COMMIT_ID}"
                            sh """
                            /kaniko/executor \
                                --dockerfile result/Dockerfile \
                                --context ${env.WORKSPACE}/result \
                                --destination ${image}
                            """
                        }
                    }
                }
            }
        }

        stage('Update and Deploy') {
            steps {
                container('kaniko') {
                    script {
                        def image = (APPLICATION == 'vote') ? "${VOTE_IMAGE}:${COMMIT_ID}" : "${RESULT_IMAGE}:${COMMIT_ID}"
                        sh """
                        kubectl set image deployment/${APPLICATION} ${APPLICATION}-container=${image}
                        kubectl rollout status deployment/${APPLICATION}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            script {
                echo 'Deployment failed, rolling back...'
                sh 'kubectl rollout undo deployment/${APPLICATION}'
            }
        }
    }
}
