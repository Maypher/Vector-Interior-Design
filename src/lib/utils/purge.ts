'use server'

const purgePath = 'http://varnish'

/**Purges the given path from the varnish cache*/
export default async function purgeRoute(path: string) {
  if (path.startsWith('/')) throw new SyntaxError(`path "${path}" cannot be absolute.`)
  await fetch(`${purgePath}/${path}`)
}
