# Vector: Interior Design Website

This is the website hosting the portfolio for [Vector: Intrior Design](https://vectorinterior.design/). 
It is written using [Nextjs](https://nextjs.org/) and [PayloadCMS](https://payloadcms.com/).

It is a rewrite of the arguably cooler and more intricate [first version](./tree/development) due to optimization issues.
This version uses Nextjs ISR functionality and nginx caching to deliver prerendered pages instead of generating the same page over
and over at request time. It also using Next's image optimization to better deliver images that are the correct size for every screen.

# Environment Variables and Secrets

## Environment Variables

| Variable   | Description                                              |
|------------|----------------------------------------------------------|
| DOMAIN     | The domain of the website (without protocol)             |
| SMTP_HOST  | The smtp host of the email address for password recovery |
| EMAIL_USER | The email address to use for password recovery           |

## Secrets

Saved in `.secrets/<secret-name>.txt`

| Secret            | Description                                          |
|-------------------|------------------------------------------------------|
| email-password    | The password of the email used for password recovery |
| payload-secret    | A random secret used for payload encryption          |
| postgres-password | The password used for the root user of the database  |

For github actions they are named using snake case `email_password`.

## Github secrets

| Secret         | Description                                           |
|----------------|-------------------------------------------------------|
| ssh_key        | The private key to connect to the VPS                 |
| ssh_connection | The ssh connection string in the form user@ip_address |

# Running

This site is deploy to a docker compose setup and can be run in any VPS. There are two ways of running this project:

- **Development:** Ran by using docker's file override system using the command `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -w`. This copies over the entire source code and enables hmr in nextjs.
- **Deployment**: Ran by using the default `docker-compose.yml` file this method using a multi stage build to only deploy the production ready code.

## Notes

Payload CMS has the ability to hot reload database changes without having to migrate. In some cases where it can't determine on its own what to do it will prompt the user. Since the promps aren't answerable through docker, in this case the nextjs server should be run locally with `npm run dev` with the environemnt variable `DATABASE_URI="postgres://postgres:<password>@localhost:5432/postgres"` set. This and `npm run payload migrate:create` should be the only reasons to run the server locally, everything else should be done through docker dev mode.