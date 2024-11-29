import { redirect } from '@sveltejs/kit';

export async function load({ fetch }) {
    let res = await fetch("/api/auth/usuario-creado");

    let user_count = parseInt(await res.text());

    if (user_count > 0) {
        redirect(302, "/cuenta")
    }
    else {
        redirect(302, "/cuenta/crear")
    }
}
