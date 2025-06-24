FROM node:20-alpine

RUN npm install -g serve

WORKDIR /home/runner/app

EXPOSE 8080

CMD ["serve", "-s", ".", "-l", "8080"]
