'use server'

const purgePath = 'http://nginx:1810/purge'

/**Purges the given path from the nginx cache*/
export default async function purgeRoute(path: string) {
  if (path.startsWith('/')) throw new SyntaxError(`path "${path}" cannot be absolute.`)
  const res = await fetch(`${purgePath}/${path}`)

  console.log(res)
  console.log(res.body)
}
