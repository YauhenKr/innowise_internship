pipeline{
    agent any
    stages {
        stage('Build the containers'){
            steps  {
                sh "docker-compose build -up",
                echo "Containers was built successfully"
                }
            }
        stage('Linters with flake8'){
            steps {
                sh 'flake8 .'
            }
        }
        stage('Test'){
            steps {
                sh 'pytest'
            }
        }
    }
}
