// pipeline{
//     agent any
//     stages {
//         stage('Build the containers'){
//             steps  {
//                 sh "docker-compose build -up"
//                 }
//             }
// //         stage('Linters with flake8'){
// //             steps {
// //                 sh "docker exec -it django bach -c 'flake8 .'"
// //             }
// //         }
// //         stage('Test'){
// //             steps {
// //                sh "docker exec -it django bach -c 'pytest'"
//         stage('Test') {
//             steps {
//                 script {
//                     // Run tests in one of the built containers
//                     def containerName = "django"
//                     sh "docker run --rm ${containerName} pytest"
                
            
//         }
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
        stage('Test'){
            steps {
//                 sh "docker-compose build -up",
                sh "docker exec -it django bash -c 'pytest'"
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
