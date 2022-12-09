package templates

import jetbrains.buildServer.configs.kotlin.Template
import jetbrains.buildServer.configs.kotlin.buildFeatures.dockerSupport

object DockerLogin : Template({
    name = "Docker Login"
    id("DockerLogin")

    features {
        dockerSupport {
            cleanupPushedImages = true
            loginToRegistry = on {
                dockerRegistryId = "PROJECT_EXT_3,PROJECT_EXT_2"
            }
        }
    }
})
