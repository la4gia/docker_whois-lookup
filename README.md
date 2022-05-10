# docker_whois-lookup

A docker continer that runs a whois lookup for specified domains in domain.yml file. 
Api is queried every 24 hours, any changes are sent to email via gmail.

Progam needs to be update with api key for https://whois.whoisxmlapi.com/, gmail address, and password. 
gmail account also needs security update to allow less secure apps. 

build with:  docker build --rm -t [docker name] .
run with: docker run -t -i -d [docker name]


