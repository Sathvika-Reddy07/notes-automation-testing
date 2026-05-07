pipeline {
    agent any


    stages {

        stage('Checkout Source Code') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Sathvika-Reddy07/notes-automation-testing.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m venv venv
                venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Parallel Test Execution') {
            steps {
                bat '''
                venv\\Scripts\\activate
                pytest -n auto
                '''
            }
        }

        stage('Generate HTML Report') {
            steps {
                bat '''
                venv\\Scripts\\activate
                pytest --html=reports/report.html --self-contained-html
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