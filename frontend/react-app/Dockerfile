FROM node:22.2-slim


WORKDIR /react-app

COPY ./package-lock.json ./

COPY ./package.json ./

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
