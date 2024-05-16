FROM amd64/node:16-alpine3.11  
  
RUN apk update && apk add vim curl bash
  
WORKDIR /usr/src/app  
  
COPY load-test.sh .  
  
CMD [ "sleep", "100000000" ]  
