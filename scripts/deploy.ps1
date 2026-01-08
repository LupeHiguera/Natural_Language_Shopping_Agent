# Deployment script for AWS
# Run from project root: .\scripts\deploy.ps1

param(
    [switch]$SkipFrontend,
    [switch]$SkipBackend,
    [switch]$SkipTerraform
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Deploying Natural Language Shopping Agent" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Step 1: Package Lambda
if (-not $SkipBackend) {
    Write-Host "`n[1/4] Packaging Lambda function..." -ForegroundColor Yellow
    Push-Location $ProjectRoot
    python scripts/package_lambda.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to package Lambda" -ForegroundColor Red
        exit 1
    }
    Pop-Location
}

# Step 2: Build Frontend
if (-not $SkipFrontend) {
    Write-Host "`n[2/4] Building frontend..." -ForegroundColor Yellow
    Push-Location "$ProjectRoot/frontend"
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to build frontend" -ForegroundColor Red
        exit 1
    }
    Pop-Location
}

# Step 3: Apply Terraform
if (-not $SkipTerraform) {
    Write-Host "`n[3/4] Applying Terraform..." -ForegroundColor Yellow
    Push-Location "$ProjectRoot/infra"
    terraform init
    terraform apply -auto-approve
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to apply Terraform" -ForegroundColor Red
        exit 1
    }

    # Capture outputs
    $BucketName = terraform output -raw frontend_bucket_name
    $DistributionId = terraform output -raw cloudfront_distribution_id
    Pop-Location
}

# Step 4: Upload frontend to S3
if (-not $SkipFrontend) {
    Write-Host "`n[4/4] Uploading frontend to S3..." -ForegroundColor Yellow

    if (-not $BucketName) {
        Push-Location "$ProjectRoot/infra"
        $BucketName = terraform output -raw frontend_bucket_name
        $DistributionId = terraform output -raw cloudfront_distribution_id
        Pop-Location
    }

    aws s3 sync "$ProjectRoot/frontend/dist" "s3://$BucketName" --delete

    Write-Host "Invalidating CloudFront cache..." -ForegroundColor Yellow
    aws cloudfront create-invalidation --distribution-id $DistributionId --paths "/*"
}

Write-Host "`n" + "=" * 60 -ForegroundColor Green
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Show important outputs
Push-Location "$ProjectRoot/infra"
Write-Host "`nImportant Information:" -ForegroundColor Cyan
Write-Host "Frontend URL: https://shop.higuera.io"
Write-Host "API URL: https://api.shop.higuera.io"
Write-Host "`nNameservers (update at your registrar):"
terraform output nameservers
Pop-Location
