FROM node:22.2-slim


WORKDIR /react-app

COPY ./package-lock.json ./

COPY ./package.json ./

RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
