pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sampreethds10/docker-app"
        DOCKER_CREDENTIALS = 'docker-hub-credentials'
        GIT_CREDENTIALS = 'github-credentials'
        HELM_CHART_PATH = './python-app'
    }

    stages {
        stage('Clone Git Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Sampreeth-DS/Docker-Pipeline.git'

                script {
                    def versionFile = readFile('version.txt').trim()
                    def versionParts = versionFile.tokenize('.')
                    def newVersion = "${versionParts[0]}.${versionParts[1].toInteger() + 1}"
                    writeFile file: 'version.txt', text: newVersion
                    env.NEW_VERSION = newVersion
                    echo "New Docker Image Version: $NEW_VERSION"
                }

                withCredentials([usernamePassword(credentialsId: GIT_CREDENTIALS, usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    script {
                        sh """
                            git config --global user.email "sampreethdsgowda@gmail.com"
                            git config --global user.name "Jenkins CI"
                            git add version.txt
                            git commit -m "Update version to $NEW_VERSION"
                            git push https://$GIT_USER:$GIT_PASS@github.com/Sampreeth-DS/Docker-Pipeline.git HEAD:main
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE:$NEW_VERSION ."
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: DOCKER_CREDENTIALS, url: '']) {
                    sh "docker push $DOCKER_IMAGE:$NEW_VERSION"
                    sh "docker tag $DOCKER_IMAGE:$NEW_VERSION $DOCKER_IMAGE:latest"
                    sh "docker rmi $DOCKER_IMAGE:$NEW_VERSION"
                }
            }
        }

        stage('Approval for the deployment') {
            steps {
                script {
                    def userInput = input message: "Do you want to deploy this version?", parameters: [
                        choice(name: 'Approval', choices: ['Approve', 'Reject'], description: 'Select Approve to proceed or Reject to stop.')
                    ]

                    if (userInput == 'Reject') {
                        error("Deployment Rejected. Stopping Pipeline.")
                    }
                }
            }
        }

        stage('Deploying Application in DEV env') {
            steps {
                script {
                    sh "helm upgrade --install python-app $HELM_CHART_PATH -n dev --set image.tag=$NEW_VERSION"
                }
            }
        }
    }
}