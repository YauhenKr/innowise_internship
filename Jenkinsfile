pipeline{
    agent any
    stages {
        stage('Build the containers'){
            steps  {
                sh "docker-compose build --no-cache"
                }
            }
        stage('Test'){
            steps {
                sh "docker-compose build --no-cache"
                sh 'docker start django'
                sh 'docker start postgresql'
//                 sh 'docker exec -i django apk add --no-cache bash'
                sh 'docker exec -i django bash -c "python manage.py migrate"'
                sh 'docker exec -i django bash -c "pytest"'
                }
            }
        stage('Linters with flake8'){
            steps {
//                 sh "docker-compose build -up",
                sh "docker exec --interactive --tty --user root django bash -c 'flake8 .'"
            }
        }
//         stage('Test'){
//             steps {
// //                 sh "docker-compose build -up",
//                 sh "docker exec -it django bash -c 'pytest'"
//                 }
//             }
        }
    }
