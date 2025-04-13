FROM node:22-alpine AS builder

WORKDIR /app/

RUN apk add --no-cache python3 make g++
COPY package*.json .
RUN npm ci

COPY . .

ARG PUBLIC_apiPath
ENV PUBLIC_apiPath=${PUBLIC_apiPath}
ARG PUBLIC_userFrontendURL
ENV PUBLIC_userFrontendURL=${PUBLIC_userFrontendURL}

RUN npm run build
RUN npm prune --production

FROM node:22-alpine AS development

WORKDIR /app/

COPY package*.json .
RUN npm install

COPY . .

ARG PUBLIC_apiPath
ENV PUBLIC_apiPath=$PUBLIC_apiPath
ENV NODE_TLS_REJECT_UNAUTHORIZED=0

ARG PUBLIC_userFrontendURL
ENV PUBLIC_userFrontendURL=${PUBLIC_userFrontendURL}

CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0",  "--port", "3000" ]

FROM node:22-alpine AS production
WORKDIR /app
COPY --from=builder /app/build/ build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json .
EXPOSE 3000

ENV NODE_ENV=production
ARG PUBLIC_apiPath
ENV PUBLIC_apiPath=${PUBLIC_apiPath}
ARG PUBLIC_userFrontendURL
ENV PUBLIC_userFrontendURL=${PUBLIC_userFrontendURL}

CMD [ "node", "build" ]
