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
                bat '''
                if not exist reports mkdir reports
                if not exist allure-results mkdir allure-results
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                if not exist reports mkdir reports

                venv\\Scripts\\python -m pytest -n 4 ^
                --html=reports\\report.html ^
                --self-contained-html ^
                --alluredir=allure-results ^
                --capture=tee-sys
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

            // 📊 HTML REPORT PUBLISH
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'HTML Test Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: false
            ])

            // 📈 ALLURE REPORT PUBLISH
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }
    }
}