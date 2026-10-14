// Jenkins pipeline for SCEMS (CI-10: Build & Deployment Scripts)
pipeline {
    agent any

    triggers {
        // Check GitHub for new commits every ~2 minutes
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build') {
            steps {
                bat 'python -m compileall scems main.py'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Package') {
            steps {
                bat 'powershell -Command "Compress-Archive -Path scems,main.py,requirements.txt,database -DestinationPath SCEMS_build_%BUILD_NUMBER%.zip -Force"'
                archiveArtifacts artifacts: 'SCEMS_build_*.zip', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "Build #${env.BUILD_NUMBER} succeeded - tests passed and package archived."
        }
        failure {
            echo "Build #${env.BUILD_NUMBER} FAILED - check the Test stage for details."
        }
    }
}
