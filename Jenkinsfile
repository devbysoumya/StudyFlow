
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python --version'
                bat 'python -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'StudyFlow tests passed!'
        }
        failure {
            echo 'StudyFlow pipeline failed. Check the console output.'
        }
    }
}
