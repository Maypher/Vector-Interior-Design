export async function load({ fetch }) {
    let res = await fetch("http://localhost:8080/auth/usuario-creado");

    let user_count = parseInt(await res.text());

    return { user_exists: user_count > 0 }
}
