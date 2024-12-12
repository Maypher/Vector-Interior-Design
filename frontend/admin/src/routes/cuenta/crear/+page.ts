import { redirect } from '@sveltejs/kit';

export async function load({ parent }) {
    let user_exists = (await parent()).user_exists;

    if (user_exists) redirect(302, "/cuenta/");
}
