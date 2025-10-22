# Check if Docker Desktop is already installed
Write-Host "Checking for existing Docker Desktop installation..."
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Docker Desktop is already installed."
} else {
    Write-Host "Docker Desktop not found. Proceeding with installation."

    # Download Docker Desktop installer
    $dockerInstallerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    $dockerInstallerPath = "$env:TEMP\DockerDesktopInstaller.exe"
    Write-Host "Downloading Docker Desktop from $dockerInstallerUrl..."
    Invoke-WebRequest -Uri $dockerInstallerUrl -OutFile $dockerInstallerPath

    # Install Docker Desktop silently
    Write-Host "Installing Docker Desktop. This may take some time..."
    Start-Process -FilePath $dockerInstallerPath -ArgumentList "install --quiet" -Wait -Verb RunAs

    # Clean up installer
    Remove-Item $dockerInstallerPath

    Write-Host "Docker Desktop installation complete. You may need to restart your machine or log out/in for Docker to be fully available."
    Write-Host "Please ensure WSL 2 is enabled and a Linux distribution is installed for optimal performance."
}

# Verify Docker installation
Write-Host "Verifying Docker installation..."
docker --version
docker-compose --version

# Example of running a docker-compose file (assuming you have a docker-compose.yml in the current directory)
Write-Host "Attempting to run docker-compose up -d (assuming docker-compose.yml exists)..."
# You should replace 'up -d' with your desired docker-compose command
# For this example, we'll just demonstrate the command execution.
# In a real scenario, you'd navigate to the directory containing your docker-compose.yml
# and then run the command.
try {
    docker-compose 
    Write-Host "docker-compose command executed successfully (dry run)."
} catch {
    Write-Host "Failed to execute docker-compose command. Ensure docker-compose.yml exists and Docker Desktop is running."
    Write-Host $_.Exception.Message
}