pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sathvika-Reddy07/notes-automation-testing.git'
            }
        }

        stage('Setup & Install Dependencies') {
            steps {
                bat '''
                python -m venv venv
                venv\\Scripts\\python -m pip install --upgrade pip
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Prepare Reports Folder') {
            steps {
                bat 'if not exist reports mkdir reports'
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                if not exist reports mkdir reports
                venv\\Scripts\\python -m pytest -n 2 --html=reports\\report.html --self-contained-html
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline Execution Completed'
        }
    }
}