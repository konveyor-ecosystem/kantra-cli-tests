# Test Application for Konveyor

This repository is intended to be used for testing Konveyor builds during CI.


## Building the application

The application has a dependency with the _corporate_ configuration-utils library. An artifact for that library has been made available using GitHub Packages in this repository and its source code is available under the _configuration-utils_ directory. [Since the Maven repository service from GitHub doesn't allow anonymous access for public packages for the moment](https://github.com/orgs/community/discussions/26634#discussioncomment-3252637), a settings.xml file like the following is required to build the application:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 http://maven.apache.org/xsd/settings-1.2.0.xsd">

  <pluginGroups>
  </pluginGroups>

  <proxies>
  </proxies>

  <servers>
    <server>
       <id>tackle-testapp-public</id>
       <username>GITHUB_USER</username>
       <password>GITHUB_TOKEN</password>
     </server>
  </servers>
  <mirrors>
    <mirror>
      <id>maven-default-http-blocker</id>
      <mirrorOf>external:http:*</mirrorOf>
      <name>Pseudo repository to mirror external repositories initially using HTTP.</name>
      <url>http://0.0.0.0/</url>
      <blocked>true</blocked>
    </mirror>
  </mirrors>
  <profiles>
    <profile>
      <id>github</id>
      <repositories>
        <repository>
          <id>central</id>
          <url>https://repo1.maven.org/maven2</url>
        </repository>
        <repository>
          <id>tackle-testapp-public</id>
          <url>https://maven.pkg.github.com/konveyor/tackle-testapp-public</url>
          <snapshots>
            <enabled>true</enabled>
          </snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>github</activeProfile>
  </activeProfiles>
</settings>
```
The Personal Access Token used for GITHUB_TOKEN [must have the read:packages scope associated](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages#about-scopes-and-permissions-for-package-registries). This scope is usually not configured by default, but can be easily changed following the step 8 detailed in the [PAT documentation from GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

Once the settings.xml file is ready, the application can be built with the following command:

```shell
mvn -s settings.xml clean package
```

If using a different settings file is not an option, there is a possibility to first build and install the configuration-utils library in the local .m2 repository:

```shell
mvn install -f ./configuration-utils
```

An then build the application itself:

```shell
mvn package -f ./configuration-utils
```


## Code of Conduct
Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
