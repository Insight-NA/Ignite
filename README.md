# How-To-IP
Guidance on the requirements and best practices for creating IP.

Our goal is to develop a portfolio of IP leveraging an open-source development model.  In order to make all projects more usable, we've developed some standards for all projects within the portfolio. All members of our organization should be able to see all repositories.  We strongly encourage all teammates to participate in IP development of all types at all levels.

## About (Description, Website, Topics)
Description: A prose description should be summarized in the about section as well.  The description can be provided from the initial repository creation or modified afterwards.

Website: The URL to the location where more detail can be found.  This might be go-to-market materials or a demoable version of the application.

Topics: Projects should be labeled with topics for findability.  Topics should outline the solution domain, technologies and problems solved by this project.

Descriptions, Website, and Topics can be updated via the gear icon in the right margin in the 'About' section.

## [Source code -> /src](./src/)
This is the primary folder where the source code for your solution should live.  If your solution is a deployment toolkit for accellerating deployments of Kubernetes it goes in /src (not /pipeline), cool new test framework? /src.

All source code should be located in the /src folder in order to keep the root folder clean. Root solution files may be located in the root folder to incorporate the other (doc, pipeline, test) folders, but the vast majority of content should be located under those sub-folders.

## [Documentation -> /doc](./doc/)
All projects should have some base level of documentation. Documentation should be put into markdown (*.md) files directly in the solution repo.  

High-level documentation should be added directly to the [README.md](./README.md) file at the root of the project with more details linking out to more detailed markdown files within relevant sub-folders.

1. High-level summary of the solution and what problem the solution solves.  Why this solution? What is unique or different about this solution that others should know about (Implements X, Y, and Z standard practices recommended by Insight or solves some unique problem)?  Reference articles or other documentation as needed to make your point.  This is your sales pitch to other developers - make it count.
2. Other project information:
   1. What type of project is this? Nuget or NPM Package? API project template? Reference architecture? Maybe multiple types...
   2. What's the status of this project? Just getting off the ground? Running at full speed / funded by a partner? Have a patent? Brag about it!
3. Overall architecture of the solution as appropriate.  Include diagrams or other reference material as needed.
4. Install & configuration of the solution.  This should be _as detailed / thorough as possible_ to give users confidence that the solution works and is easy to use.  Reference deployment templates as needed.
5. How to use the solution - reference example solutions as needed
6. Troubleshooting & Issues - outline any common pitfalls and specify additional information requested to ease triaging issues
7. Code documentation - all projects should include "triple-slash" or JavaDoc (or similar for the chosen technology) comments and documentation.

## [Testing -> /test](./test/)
Testing of the source solution is required for all IP development to ensure that our teammates using our solutions will be leveraging a solution that "just works".  Tests should be located under the /test folder and 'portable' tests (i.e. unit tests) should be automatically run within each pull request at a minimum.  More detailed test recommendations are outlined in the [test folder readme](./test/).

## [Sample Solutions -> /samples](./samples/)
Samples demonstrate how the solution would work in real scenarios.  Samples should be provided in fully working solutions that can be downloaded and run or deployed (in the case of deployable services) on their own to demonstrate the working solution.

## [Artifact Build & Release -> /.github](./.github/)
Artifacts should be built and published into the organization artifact repository. Artifacts can be released as as needed but should always be published via a CD pipeline.  The artifact repository supports Nuget, NPM, Containers, Docker, Maven, and RubyGems.

Artifacts should be versioned in some appropriate incrementing fashion.  Sequential versions, Semantic versioning, or date versioning are all appropriate ways to version artifacts.

Above high-level solution documentation should be provided on build artifact metadata or manifests as well.  This is critical for supporting clients that will use build artifacts but may not have access to the full source repository.

## [Deployment Templates -> /pipeline](./pipeline/)
Deployment templates should be provided for any solution that produces a deployable service.  Ideally templates would include Azure ARM, AWS CloudFormation, GCP Deployment Manager, and Hashicorp Terraform templates.  In reality developing all four templates is unlikely, however since each client may favor different IaC tools and cloud providers it is preferrable to have many different types of templates available for delivery teams to leverage.

## [Issue Tracking & Support](../../issues)
We recommend that all projects identify teams of contributors who will support usage of the solution for other delivery teammates.  We encourage the use of GitHub issues to open and track bugs and other support questions and are looking into tying issue tracking into teams channels for more effective collaboration/communication.

The larger/more complex the solution, the more need there will be for support; please be aware that projects completely devoid of support will likely get little to no use.  Some basic support indicators are:
- How quickly do issues get responded to?
- How many open issues/bugs are there?
- When was the last time a commit was made to this repo?
- How long do pull requests sit before being approved / commented?

With all of the above, the more collaborators and contributors you have on your project the better off you'll be.  Please encourage participation from others in the org.  Teamwork makes the dream work.
