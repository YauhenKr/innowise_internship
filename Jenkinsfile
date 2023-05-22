// pipeline{
//     agent any
//     stages {
//         stage('Build the containers'){
//             steps  {
//                 sh "docker-compose build --no-cache"
//                 }
//             }
//         stage('Test'){
//             steps {
//                 sh "docker-compose build --no-cache"
//                 sh 'docker start django'
//                 sh 'docker start postgresql'
// //                 sh 'docker exec -i django apk add --no-cache bash'
//                 sh 'docker exec -i django bash -c "python manage.py migrate"'
//                 sh 'docker exec -i django bash -c "pytest"'
//                 }
//             }
//         stage('Linters with flake8'){
//             steps {
// //                 sh "docker-compose build -up",
//                 sh "docker exec --interactive --tty --user root django bash -c 'flake8 .'"
//             }
//         }
// //         stage('Test'){
// //             steps {
// // //                 sh "docker-compose build -up",
// //                 sh "docker exec -it django bash -c 'pytest'"
// //                 }
// //             }
//         }
//     }

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    // Определение пути до файла docker-compose.yml
                    def dockerComposeFile = 'docker-compose.yml'
                    
                    sh "docker-compose -f ${dockerComposeFile} down"

                    // Запуск команды docker-compose up для сборки контейнеров
                    sh "docker-compose -f ${dockerComposeFile} up -d"
                    // Ожидание некоторого времени, чтобы контейнеры успели запуститься

                    // Вывод журналов контейнеров
                    sh "docker-compose -f ${dockerComposeFile} logs"

                    // Проверка статуса контейнеров
                    def containerStatus = sh(script: "docker-compose -f ${dockerComposeFile} ps -q | xargs docker inspect -f '{{ .State.Status }}'", returnStdout: true)

                    // Проверка, успешно ли запущены все контейнеры
                    if (containerStatus.trim().contains('running')) {
                        echo 'Все контейнеры были успешно запущены.'
                    } else {
                        error 'Не удалось запустить все контейнеры.'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Проверка наличия контейнера с PostgreSQL
                    def postgresContainer = sh(script: "docker-compose ps -q db_postgresql", returnStdout: true).trim()

                    if (postgresContainer) {
                        echo "Контейнер с PostgreSQL запущен."
                        // Вывод списка таблиц
                        sh "docker exec -i postgresql psql -U postgres -c '\\dt'"
                    } else {
                        error "Контейнер с PostgreSQL не найден."
                    }
                    sh 'sleep 15'
                    // Запуск тестов с помощью pytest
                    sh "docker exec -i django python manage.py makemigrations"
                    sh "docker exec -i django python manage.py migrate"
                    sh "docker exec -i django python manage.py migrate django_celery_results"

                    sh "docker exec -i django pytest"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'pwd' // Вывод текущего каталога
                sh 'sudo docker build -t forartsake/petinnowise:latest .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhubaccount', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push forartsake/petinnowise:latest'
            }
        }
    }

    post {
        always {
            // Завершение и очистка контейнеров после выполнения пайплайна
            script {
                def dockerComposeFile = './docker-compose.yml'

                // Остановка и удаление контейнеров
                sh "docker-compose -f ${dockerComposeFile} down"
            }
        }
    }
}
