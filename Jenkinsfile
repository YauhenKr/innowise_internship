pipeline {
    agent any
    stages {
//         stage('Build') {
//             steps {
//                 script {
//                     // Определение пути до файла docker-compose.yml
//                     def dockerComposeFile = 'docker-compose.yml'
                    
//                     // Запуск команды docker-compose up для сборки контейнеров
//                     sh "sudo docker-compose -f ${dockerComposeFile} up -d"
//                     // Ожидание некоторого времени, чтобы контейнеры успели запуститься

//                     // Вывод журналов контейнеров
//                     sh "docker-compose -f ${dockerComposeFile} logs"

//                     // Проверка статуса контейнеров
//                     def containerStatus = sh(script: "docker-compose -f ${dockerComposeFile} ps -q | xargs docker inspect -f '{{ .State.Status }}'", returnStdout: true)

//                     // Проверка, успешно ли запущены все контейнеры
//                     if (containerStatus.trim().contains('running')) {
//                         echo 'Все контейнеры были успешно запущены.'
//                     } else {
//                         error 'Не удалось запустить все контейнеры.'
//                     }
//                 }
//             }
//         }

//         stage('Test') {
//             steps {
//                 script {
//                     // Проверка наличия контейнера с PostgreSQL
//                     def postgresContainer = sh(script: "docker-compose ps -q postgresql", returnStdout: true).trim()

//                     if (postgresContainer) {
//                         echo "Контейнер с PostgreSQL запущен."
//                         // Вывод списка таблиц
//                         sh "docker exec -i postgresql psql -U postgres -c '\\dt'"
//                     } else {
//                         error "Контейнер с PostgreSQL не найден."
//                     }
//                     sh 'sleep 15'
//                     // Запуск тестов с помощью pytest
//                     sh "docker exec -i django python manage.py makemigrations"
//                     sh "docker exec -i django python manage.py migrate"
//                     sh "docker exec -i django python manage.py migrate django_celery_results"
//                     sh "docker exec -i django pytest"
//                 }
//             }
//         }

        stage('Docker Login') {
            steps {
              withCredentials([usernamePassword(credentialsId: 'dockerhubaccount', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
              }
            }
          }

        stage('Build') {
            steps {
              sh 'sudo docker-compose build'
              sh 'sudo docker ps'
            }
          }

//         stage('Rename') {
//             steps {
//               sh 'docker tag celery_worker:latest yauhenkryvanos/celery_worker:latest'
//               sh 'docker tag django:latest yauhenkryvanos/django:latest'
//             }
//           }

        stage('Push') {
            steps {
              sh 'docker push yauhenkryvanos/celery_worker:latest'
              sh 'docker push yauhenkryvanos/django_petproject:latest'
            }
          }
        }
      }
