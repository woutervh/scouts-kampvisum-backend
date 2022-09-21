pipeline {
  agent any

  options {
    buildDiscarder(logRotator(artifactNumToKeepStr: '10'))
  }

  stages {
    stage('deploy') {
      steps {
        sh 'ssh az-deb-mgmt sudo -u ansible /opt/deploy-kamp.sh backend ${BRANCH_NAME}'
      }
    }
  }

  post {
    failure {
      emailen()
    }
    unstable {
      emailen()
    }
    changed {
      emailen()
    }
  }
}

def emailen() {
  mail(
    to: "tvl@scoutsengidsenvlaanderen.be,${env.CHANGE_AUTHOR_EMAIL}, boro@inuits.eu",
    subject: "[Jenkins] ${currentBuild.fullDisplayName} ${currentBuild.currentResult}",
    body: """${currentBuild.fullDisplayName} ${currentBuild.currentResult}

${currentBuild.absoluteUrl}"""
  )
}
