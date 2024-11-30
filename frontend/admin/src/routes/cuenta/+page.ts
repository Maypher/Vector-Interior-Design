import { redirectWithToast } from '$lib/utilities/toasts.js';

export async function load({ parent }) {
    let user_exists = (await parent()).user_exists;

    if (!user_exists) redirectWithToast("/cuenta/crear/", "Ningún usuario encontrado. Por favor crear uno.", "WARNING");
}
