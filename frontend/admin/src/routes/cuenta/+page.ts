import { redirect } from '@sveltejs/kit';
import { superValidate } from "sveltekit-superforms";
import { yup } from "sveltekit-superforms/adapters";
import { loginSchema } from '$lib/utilities/yupSchemas.js';

export async function load({ parent }) {
    let user_exists = (await parent()).user_exists;

    if (!user_exists) redirect(302, "/cuenta/crear/");

    const loginForm = await superValidate(yup(loginSchema));

    return { loginForm };
}
