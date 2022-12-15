pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
    }
    stages {
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                withCredentials(
                    [
                        string(credentialsId: 'BESTBUY_STEELBOOKS_PASSWORD', variable: 'BESTBUY_STEELBOOKS_PASSWORD'),
                        string(credentialsId: 'FROM_EMAIL', variable: 'FROM_EMAIL'),
                        string(credentialsId: 'TO_EMAIL', variable: 'TO_EMAIL')
                    ]
                ) {
                    sh label: '', script: """bash -c \'
                        export BESTBUY_STEELBOOKS_PASSWORD=${BESTBUY_STEELBOOKS_PASSWORD};
                        export FROM_EMAIL=${FROM_EMAIL};
                        export TO_EMAIL=${TO_EMAIL};
                        echo 'BESTBUY_STEELBOOKS_PASSWORD='"'"${BESTBUY_STEELBOOKS_PASSWORD}"'" > chomp.env
                        echo 'FROM_EMAIL='"'"${FROM_EMAIL}"'" >> chomp.env
                        echo 'TO_EMAIL='"'"${TO_EMAIL}"'" >> chomp.env
                        docker-compose -f docker-compose.yml up -d  --force-recreate --build
                    \'"""
                }
            }
        }
    }
    post {
      always {
          script {
              if (fileExists('test_results/all-unit-tests.xml')){
                  junit skipPublishingChecks: true, testResults: 'test_results/all-unit-tests.xml'
              }
          }
      }
  }
}
