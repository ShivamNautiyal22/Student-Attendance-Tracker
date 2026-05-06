pipeline {
    agent any

    environment {
        AWS_REGION     = 'eu-west-2'
        ECR_REPO       = 'student-tracker'
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
        ECR_URI        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
        APP_EC2_IP     = credentials('APP_EC2_IP')
        SSH_KEY        = credentials('EC2_SSH_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${ECR_REPO}:latest ."
            }
        }

        stage('Push to ECR') {
            steps {
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_URI}
                    docker tag ${ECR_REPO}:latest ${ECR_URI}:latest
                    docker push ${ECR_URI}:latest
                """
            }
        }

        stage('Deploy to App EC2') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no -i ${SSH_KEY} ubuntu@${APP_EC2_IP} '
                        aws ecr get-login-password --region eu-west-2 | \
                        docker login --username AWS --password-stdin ${ECR_URI}
                        docker pull ${ECR_URI}:latest
                        docker stop student-tracker || true
                        docker rm student-tracker || true
                        docker run -d --name student-tracker -p 80:8000 \
                            --env-file /home/ubuntu/app.env \
                            ${ECR_URI}:latest
                    '
                """
            }
        }
    }

    post {
        success { echo 'Deployed successfully!' }
        failure  { echo 'Build failed. Check logs.' }
    }
}