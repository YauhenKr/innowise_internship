// pipeline{
//     agent any
//     stages {
//         stage('Build the containers'){
//             steps  {
//                 sh "docker-compose build -up"
//                 }
//             }
//         stage('Linters with flake8'){
//             steps {
//                 sh "docker exec -it django bach -c 'flake8 .'"
//             }
//         }
//         stage('Test'){
//             steps {
//                 sh "docker exec -it django bach -c 'pytest'"
//             }
//         }
//     }
// }

pipeline{
    agent any
    stages {
        stage('Build the containers'){
            steps  {
                sh "docker-compose build -up"
                }
            }
//         stage('Linters with flake8'){
//             steps {
//                 sh "docker-compose build -up",
//                 sh "docker exec -it django bach -c 'flake8 .'"
//             }
//         }
//         stage('Test'){
//             steps {
//                 sh "docker-compose build -up",
//                 sh "docker exec -it django bach -c 'pytest'"
       stage('Build and test') {
        steps {
            script {
                def app_image = docker.build('my-app')
                app_image.inside {
                    sh "docker-compose build -up"
                    }
                def test_image = docker.build('my-app-tests')
                test_image.inside {
                    sh "docker exec -it django bach -c 'pytest'"
                }
            }
        }
    }
}
}
