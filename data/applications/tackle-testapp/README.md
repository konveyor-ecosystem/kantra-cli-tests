# Test Application for Tackle

This repository is intended to be used for testing the Git, Maven and Subversion integration developed for Tackle.


## Testing Git integration

This is a private repository with one branch. That should cover the authentication scenario and the usage of branches.

## Testing Maven integration

An artifact has been made available using GitHub Packages in this repository. To access the artifact, a settings.xml file like the following will be required:

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
       <id>tackle-testapp</id>
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
          <id>tackle-testapp</id>
          <url>https://maven.pkg.github.com/konveyor/tackle-testapp</url>
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
The user corresponding to the value of GITHUB_USER must have access to the private repository. The Personal Access Token used for GITHUB_TOKEN [must have the read:packages scope associated](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages#about-scopes-and-permissions-for-package-registries). This scope is usually not configured by default, but can be easily changed following the step 8 detailed in the [PAT documentation from GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). It would be desirable to setup a service account for this and add it as a collaborator in the project, rather than having to add more individual collaborators.

Once the settings.xml file is ready, the artifact can be downloaded with the following command:

```shell
mvn -s settings.xml dependency:copy -Dmdep.useBaseVersion=true -DoutputDirectory=$HOME/binaries -Dartifact=io.konveyor.demo:customers-tomcat:0.0.1-SNAPSHOT:war
```

## Testing Subversion Integration

[GitHub has a Subversion bridge that allows using Subversion clients transparently to access a Git repository](https://docs.github.com/en/get-started/importing-your-projects-to-github/working-with-subversion-on-github/support-for-subversion-clients). This means that this repository can be used to test Subversion integration as well. With the following command, GitHub will respond as if the client was dealing with a real Subversion server:

```shell
svn checkout https://github.com/rromannissen/tackle-testapp
```
