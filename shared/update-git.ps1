# run from src folder for year
#
$commit_comment = Read-Host "Commit comment"
if(-not($commit_comment)){
  Write-output "Enter commit comment" 
    Exit
}

Write-output "Updating git..." 

git add *.py
git add ../data/*.txt
attrib +r ../data/*.txt
git commit -am $commit_comment
git push -u origin main

Write-output "Done"
