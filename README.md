# Reference-based Tree Structure (RBTS) Blockchain

***The following content is copied from my Master Thesis.  
The links to cited content can be found in the thesis itself.***

## Docker image

The desired image derives from the popular variation of Linux distribution — Alpine Linux. It's a perfect choice due to the nature of the application and the only significant requirement of Python 3.9, and its package manager *pip*. Image is small, secure, efficient on resources, and contains everything that's needed. After building, the image size is only about 100 megabytes.

The process of embedding the program into the future container is quite simple. Firstly, all the files are copied onto the image. The configuration file `config.yaml` is treated as a volume, which means that for more comfortable use one can mount their own configuration file instead of overwriting the one bundled with the project. Next, the required packages are installed from `requirements.txt`. In the end, the program is being run with command `python3 main.py`. This implies that the container will exit immediately upon finishing the program, producing an output to the *stdout* if the flag *-it* had been passed to the *docker* command. Saving output to file can be done in *Bourne Again Shell (bash)* by redirecting the *stdout* file descriptor to a particular file. 

The mentioned instructions mapped to the `Dockerfile` are shown in Listing 1.
```Dockerfile
FROM python:3.9-alpine

COPY . .
VOLUME "config.yaml"
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
```
<div align="center">Listing 1.</div>
<br/>
  
## Steps to recreate the research
In order to recreate the experiment on a local machine, one has to use an operating system that supports Docker. The solution should work on the most popular ones, like Linux, macOS, or Windows. 

The first step is to download the newest Docker. On Linux, it can be done directly from the terminal with the tool *wget* and the Bourne Again Shell often referred to as *bash*. The commands are provided for Ubuntu 20.04, a popular Linux distribution with APT package manager and systemd. The instructions to write in shell are presented in Listing 2. The `sudo` keyword can be omitted if the user has logged in as a root user.
```bash
# Getting needed tools
sudo apt update
sudo apt install -y curl 

# Downloading the script
curl -fsSL https://get.docker.com -o get-docker.sh

# Installing the Docker
sh get-docker.sh

# Starting the Docker
sudo systemctl start docker
```
<div align="center">Listing 2.</div>
<br/>
  
Installation of Windows or macOS machine is done by downloading the installer of Docker Desktop and proceeding with the instructions on the screen. 

After installing Docker, the next step is to download the zip archive from the git repository stored on the GitHub platform and unpack it. In order to do it on Linux, commands from Listing 3 can be run. They should also work on macOS systems, otherwise, they can be done in a similar fashion as on Windows OS. To download and unpack repository on a Windows machine, one has to open the link in the web browser, in file manager right-click on the archive and select the option most similar to “extract here”.

```shell
# Getting the archive  
ZIP_ROUTE="matgd/tree-structure-blockchain/archive/refs/heads/master.zip/"
curl -fsSL https://github.com/${ZIP_ROUTE} -o blockchain-tree-structure.zip

# Unpacking the archive
unzip blockchain-tree-structure.zip
```
<div align="center">Listing 3.</div>
<br/>  

Afterwards, all that's left for recreating the results is to build the image from the Dockerfile and start up the container. Inside the just unpacked directory in the archive, `blockchain-tree-structure-master`, one has to type shown commands in Listing 4.

```shell
# Go to unzipped directory with the Dockerfile
cd blockchain-tree-structure-master

# Build the Docker image
docker build -t blockchain-tree:1.0 .

# Run container with default configuration
docker run -it --name blockchain-tree blockchain-tree:1.0

# Run container with custom configuration
#    on Windows, when using 'cmd' instead of 'PowerShell', 
#    replace '${PWD}' with '%cd%'
#
# docker run -it -v ${PWD}/config2.yaml:/config.yaml --name blockchain-tree blockchain-tree:1.0

# Copy execution time to host
docker cp blockchain-tree:/exec_time.csv exec_time_container.csv

# Remove container
docker container rm -f blockchain-tree  

# Remove image
docker image rm blockchain-tree:1.0
```
<div align="center">Listing 4.</div>
<br/>  
