FROM node:lts as base

FROM base as compile

WORKDIR /build/

COPY . .

RUN npm install

RUN npm run build

FROM base as dev

WORKDIR /app/

COPY . .

RUN npm install

CMD ["npm", "run", "dev"]

FROM base as prod

WORKDIR /app/

COPY package*.json .
COPY --from=compile /build/dist/ .

RUN export NODE_ENV=production

RUN npm install

CMD ["npm", "run", "prod"]
