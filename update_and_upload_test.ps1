#!/bin/pwsh

. .\env\Scripts\activate
$Folder = "dist"
if (Test-Path -Path $Folder) {
    Remove-Item	dist -Recurse -Force -Confirm:$false
}
py -m build
py -m twine upload --repository testpypi dist/*