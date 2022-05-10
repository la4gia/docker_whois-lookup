# Docker Container whois-api lookup

A docker container that runs a whois lookup for specified domains in domain.yml file. 
API is queried every 24 hours, any changes are sent to email via gmail.

Program needs to be update with api key for https://whois.whoisxmlapi.com/, gmail address, and password. 
The gmail account also needs security settings changed to allow 'less secure apps' functionality. 

build with:  docker build --rm -t [docker name] .
run with: docker run -t -i -d [docker name]


