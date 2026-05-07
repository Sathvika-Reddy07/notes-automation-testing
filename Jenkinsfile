pipeline {
    agent any

    stages {

        stage('Checkout Source Code') {
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

        stage('Run Tests (Parallel Execution)') {
            steps {
                bat '''
                venv\\Scripts\\python -m pytest -n 2 --html=reports/report.html --self-contained-html
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'reports/**, logs/**, screenshots/**', fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline Execution Completed'
        }
    }
}