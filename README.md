# Confpoint (Confluence / SharePoint) tools

This module contains a set of CLI utils for working with the Atlassian Confluence and the Microsoft SharePoint.
It contains three submodules: *publisher, uploader, downloader*.

![console](https://github.com/Mcublog/confpoint/raw/master/doc/2022-03-13_18-44.gif)

----------------------------------------------------------------

* **publisher** module allowed to you a public and remove Confluence page. The page creating from markdown file.

Using example (*PowerShell script*):

```PowerShell
py -m confpoint.publisher --user "user@mail.com" --apikey "123abc" `
                          --space "your space" `
                          --parent "parent page (optional)" `
                          --title "title page in Confluence" `
                          --file "*.MD file which will be published" `
                          --link "https://your_domain.atlassian.net"
```

----------------------------------------------------------------

* **uploader** module allowed to you upload a file or directory to the SharePoint server.

Using example (*PowerShell script*):

```PowerShell
py -m confpoint.uploader --user "user@mail.com" --password "pass" `
                         --file "path/to/uploading/file" `
                         --remote "remote/path/in/SharePoint/server" `
                         --group "your sharepoint group (somthing like /sites/Team)" `
                         --link "https://your_domain.sharepoint.com" `
                         --timeout 10
```

----------------------------------------------------------------

* **downloader** module allowed to you download a file or directory from the SharePoint server. Also support recursive downloading content from directory.

Using example (*PowerShell script*):

```PowerShell
py -m confpoint.downloader --user "user@mail.com" --password "pass" `
                           --outputdir "path/to/local/output/directory" `
                           --remote "remote/path/in/SharePoint/server" `
                           --group "your sharepoint group (somthing like /sites/Team)" `
                           --link "https://your_domain.sharepoint.com" `
                           --recursive
```

## Usefully notes

* For building .exe file:

  ```terminal
  ./py2exe.ps1
  ```

* Create virtual env and activate it

  ```terminal
  py -m venv env
  .\env\Scripts\activate
  ```

* Install from [TestPyPi](https://test.pypi.org/):

  ```terminal
  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple confpoint
  ```

## Usefully notes and links

* Install dependency: pip3 install -r requerments.txt
* Get token for confluence.[Check this arcticle](https://docs.searchunify.com/Content/Content-Sources/Atlassian-Jira-Confluence-Authentication-Create-API-Token.htm) [or this](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)
* For upload files to SharePoint use your login and password (login == --user; password == --apikey)
* Open file pusher.cmd and write your login, token and etc
* Docker imgage with [Confpoint and PowerShell](https://github.com/Mcublog/confpoint-docker)
