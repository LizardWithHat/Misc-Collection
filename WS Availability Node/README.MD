This node project will query specified computers in your network to check if they are online and what users are logged into them. That way you can build a list of available Workstations and their available Software (staticly listed) that will always be up to date.

For that the executing Server needs to be a windows computer with the neccessary permissions to query a computer. Internally the "query user /server:<SERVER>" command is used to accomplish this.

The Workstations are queried asynchronly and will update the different parts of the website as soon as there is an answer, or the lack of one.

To use this properly on an Windows Server, you can use tools like [NSSM](https://nssm.cc/) to install your own Windows Service to monitor and control it accordingly.