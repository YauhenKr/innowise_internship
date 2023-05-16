pipeline{
    agent any
    stages {
        stage('Build the containers'){
            steps  {
                sh "docker-compose build -up"
                }
            }
        stage('Linters with flake8'){
            steps {
                sh "docker exec -it django bach -c 'flake8 .'"
            }
        }
        stage('Test'){
            steps {
                sh "docker exec -it django bach -c 'pytest'"
            }
        }
    }
}
