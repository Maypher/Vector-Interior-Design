import { redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { signUpForm } from '$lib/utilities/yupSchemas.js';

export async function load({ parent }) {
    let user_exists = (await parent()).user_exists;
    if (user_exists) redirect(302, "/cuenta/");

    const createForm = await superValidate(yup(signUpForm));

    return { createForm };
}
