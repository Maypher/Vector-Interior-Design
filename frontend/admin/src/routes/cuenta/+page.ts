import { superValidate } from "sveltekit-superforms";
import { yup } from "sveltekit-superforms/adapters";
import { loginSchema } from '$lib/utilities/yupSchemas.js';

export async function load() {
    const loginForm = await superValidate(yup(loginSchema));

    return { loginForm };
}
