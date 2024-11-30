import { redirectWithToast } from '$lib/utilities/toasts.js';

export async function load({ parent }) {
    let user_exists = (await parent()).user_exists;

    if (user_exists) redirectWithToast("/cuenta/", "Cuenta principal ya creada. Por favor iniciar sesión.", "WARNING");
}
