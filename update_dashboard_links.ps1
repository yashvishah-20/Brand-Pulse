$files = @(
    "dashboard_instagram2.html",
    "dashboard_reddit2.html", 
    "dashboard_marketbeat2.html",
    "dashboard_glassdoor2.html",
    "dashboard_stocktwits2.html",
    "dashboard_linkedin2.html",
    "dashboard_google2.html"
)

$basePath = "C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\brandmeter\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\pages\"

foreach ($file in $files) {
    $filePath = $basePath + $file
    Write-Host "Processing $file..."
    
    # Read the file content
    $content = Get-Content $filePath -Raw
    
    # Replace dashboard_overview.html with dashboard_overview2.html
    $content = $content -replace 'dashboard_overview\.html', 'dashboard_overview2.html'
    
    # Replace all platform links to use the "2" versions
    $content = $content -replace 'dashboard_facebook\.html', 'dashboard_facebook2.html'
    $content = $content -replace 'dashboard_x\.html', 'dashboard_x2.html'
    $content = $content -replace 'dashboard_google\.html', 'dashboard_google2.html'
    $content = $content -replace 'dashboard_instagram\.html', 'dashboard_instagram2.html'
    $content = $content -replace 'dashboard_reddit\.html', 'dashboard_reddit2.html'
    $content = $content -replace 'dashboard_marketbeat\.html', 'dashboard_marketbeat2.html'
    $content = $content -replace 'dashboard_glassdoor\.html', 'dashboard_glassdoor2.html'
    $content = $content -replace 'dashboard_stocktwits\.html', 'dashboard_stocktwits2.html'
    $content = $content -replace 'dashboard_linkedin\.html', 'dashboard_linkedin2.html'
    
    # Write the updated content back to the file
    Set-Content $filePath -Value $content -Encoding UTF8
    
    Write-Host "Updated $file"
}

Write-Host "All files updated successfully!"
