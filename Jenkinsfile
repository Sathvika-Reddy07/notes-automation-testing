// Jenkins Declarative Pipeline for Notes Automation Testing Framework

pipeline {

    // Run pipeline on any available Jenkins agent
    agent any

    stages {

        // STAGE 1: SOURCE CODE CHECKOUT
   
        stage('Checkout') {
            steps {
                // Pull latest code from main branch of GitHub repository
                git branch: 'main',
                    url: 'https://github.com/Sathvika-Reddy07/notes-automation-testing.git'
            }
        }

        // STAGE 2: ENVIRONMENT SETUP & DEPENDENCY INSTALLATION
  
        stage('Setup & Install Dependencies') {
            steps {
                bat '''
                # Create isolated Python virtual environment for test execution
                python -m venv venv

                # Upgrade pip inside virtual environment for stable package resolution
                venv\\Scripts\\python -m pip install --upgrade pip

                # Install all required dependencies from requirements file
                venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        // STAGE 3: REPORT DIRECTORY PREPARATION

        stage('Prepare Reports Folder') {
            steps {
                bat '''
                # Ensure reports directory exists for HTML reports
                if not exist reports mkdir reports

                # Ensure Allure results directory exists for structured test reporting
                if not exist allure-results mkdir allure-results
                '''
            }
        }


        // STAGE 4: TEST EXECUTION

        stage('Run Tests') {
            steps {
                bat '''
                # Ensure reports folder exists before execution (safety check)
                if not exist reports mkdir reports

                # Execute pytest test suite with parallel execution enabled
                # -n 4 enables 4 parallel workers for faster execution
                venv\\Scripts\\python -m pytest -n 4 ^
                --html=reports\\report.html ^                 
                --self-contained-html ^                      
                --alluredir=allure-results ^                 
                --capture=tee-sys                            
                '''
            }
        }

        // STAGE 5: ARCHIVE ARTIFACTS

        stage('Archive Artifacts') {
            steps {
                // Store test reports in Jenkins build artifacts for later access
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }
        }
    }

    // POST EXECUTION ACTIONS (ALWAYS RUN)

    post {
        always {

            // Log pipeline completion status in console output
            echo 'Pipeline Execution Completed'

      
            // HTML REPORT PUBLISHING
    
            publishHTML([
                reportDir: 'reports',                    // Directory containing HTML report
                reportFiles: 'report.html',              //Main report file
                reportName: 'HTML Test Report',          //Display name in Jenkins UI
                keepAll: true,                           //Keep reports for all builds
                alwaysLinkToLastBuild: true,             //Quick access to latest report
                allowMissing: false                      //Fail if report is not generated
            ])

            // ALLURE REPORT PUBLISHING
            allure([
                includeProperties: false,                //Skip extra properties file
                jdk: '',                                 //Use default Jenkins JDK
                results: [[path: 'allure-results']]      //Path to Allure raw results
            ])
        }
    }
}