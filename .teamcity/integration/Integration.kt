package integration

import common.git.publishCommitShortSha
import common.python.buildPythonPackage
import common.python.publishPythonPackageToHosted
import jetbrains.buildServer.configs.kotlin.BuildType
import jetbrains.buildServer.configs.kotlin.DslContext
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import templates.DockerLogin

class Integration(
    dockerToolsTag: String
) : BuildType({
    templates(DockerLogin.create())

    id("Integration")
    name = "Integration"
    allowExternalStatus = true

    vcs {
        root(DslContext.settingsRoot)
        cleanCheckout = true
        branchFilter = """
            +:*
        """.trimIndent()
    }

    triggers {
        vcs {
            branchFilter = """
                +:*
            """.trimIndent()
        }
    }

    steps {
        publishCommitShortSha()
        buildPythonPackage(dockerToolsTag)
        publishPythonPackageToHosted(dockerToolsTag)
    }

    artifactRules = """
        dist/*.whl
        dist/PKG-INFO.txt
    """.trimIndent()

    params {
        param("teamcity.vcsTrigger.runBuildInNewEmptyBranch", "true")
    }
})
