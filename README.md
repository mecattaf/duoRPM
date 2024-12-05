# Automated Fedora COPR Repository Management with GitHub Actions

This guide explains how to set up and maintain Fedora COPR repositories using GitHub Actions for automated builds and updates. This approach allows you to manage your RPM packages through Git while automating the build and publication process.

## Acknowledgments

This workflow draws significant inspiration from [solopasha's hyprlandRPM repository](https://github.com/solopasha/hyprlandRPM), which demonstrates excellent practices for COPR repository management through GitHub Actions.

## Prerequisites

Before starting, ensure you have:
- A Fedora account
- Basic knowledge of RPM packaging
- A GitHub account
- Your RPM spec files ready (you can use tools like rust2rpm, pyp2rpm, gem2rpm, gofed, or npm2rpm to help create these)

## Setting Up COPR Authentication

1. Visit https://copr.fedorainfracloud.org/api/
2. Generate an API token
3. In your GitHub repository:
   - Navigate to Settings → Secrets and Variables → Actions
   - Create a new repository secret named `COPR_CONFIG`
   - Add your COPR configuration content:
   ```ini
   [copr-cli]
   login = <your_copr_username>
   username = <your_copr_username>
   token = <your_token>
   copr_url = https://copr.fedorainfracloud.org
   ```

## Creating Your COPR Repository

### Through the Fedora Web UI (Recommended)

1. Go to https://copr.fedorainfracloud.org/ and log in
2. Click "New Project"
3. Configure your project settings:
   - Name: Your repository name
   - Description: Brief description of your package collection
   - Visibility: Set to "public"
   
4. Build Options:
   - Select "fedora-* x86_64" for all current Fedora versions
   - Create repositories manually: Unchecked
   - Enable internet access during builds: Checked
   - Project will not be listed on home page: Unchecked
   - Follow Fedora branching: Checked
   - Multilib support: Checked
   - Repository contains module hotfixes: Unchecked
   - Run fedora-review tool: Checked
   - Generate AppStream metadata: Checked
   - Build isolation: Use default configuration from mock-core-configs.rpm

### Alternative: Command Line Setup

If you prefer using the command line:
```bash
copr-cli create your-repo-name --chroot fedora-rawhide-x86_64 --description "Your repository description"
```

## GitHub Repository Configuration

1. Enable GitHub Actions:
   - Go to Settings → Actions → General
   - Enable "Read and write permissions" under "Workflow permissions"
   - Allow GitHub Actions to create and approve pull requests

2. Make workflow files executable:
```bash
chmod +x .github/workflows/*.yml
chmod +x */update.sh
```

## Initial Repository Setup and Build

1. Push your changes to GitHub:
```bash
git add .
git commit -m "Initial repository setup [build-all]"
git push
```

The `[build-all]` tag in the commit message triggers the initial build of all packages.

## Monitoring Your Setup

1. Watch the GitHub Actions tab in your repository
   - Verify both update and build workflows run successfully
   - The update workflow checks for new versions
   - The build workflow submits packages to COPR

2. Monitor builds at: https://copr.fedorainfracloud.org/coprs/yourusername/your-repo-name/
   - Packages will build in dependency order
   - Build status and logs are available for each package

## Success Criteria

Your setup is working correctly when you see:
- Green checkmarks in GitHub Actions
- Successful builds in COPR
- A repository that can be enabled on Fedora systems

## Maintaining Your Repository

The GitHub Actions workflows will:
- Automatically check for updates to your packages
- Create pull requests when updates are available
- Trigger builds when changes are merged
- Manage the build order based on dependencies

Your COPR repository is now set up for automated maintenance, with builds triggered by commits and version updates handled automatically through GitHub Actions.
