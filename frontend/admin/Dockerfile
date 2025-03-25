FROM node:22-alpine AS builder

WORKDIR /app/

COPY package*.json .
RUN npm ci

COPY . .

ARG PUBLIC_apiURL
ENV PUBLIC_apiURL=${PUBLIC_apiURL}
RUN npm run build
RUN npm prune --production

FROM node:22-alpine AS development

WORKDIR /app/

COPY package*.json .
RUN npm install

COPY . .

ARG PUBLIC_apiURL
ENV PUBLIC_apiURL=$PUBLIC_apiURL
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0",  "--port", "80" ]

FROM node:22-alpine AS production
WORKDIR /app
COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production

CMD [ "node", "build" ]
