export async function load({ fetch }) {
    let res = await fetch("/api/auth/usuario-creado");

    let user_count = parseInt(await res.text());

    return { user_exists: user_count > 0 }
}
