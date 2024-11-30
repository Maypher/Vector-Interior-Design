import { type UserData } from "$lib/utilities/interfaces";
import { redirectWithToast } from '$lib/utilities/toasts.js';

export async function load({ fetch }) {
    // Determine if user is logged in
    let res = await fetch("/api/auth/info-usuario");

    if (res.status != 200) redirectWithToast("/cuenta/", "No existe sesión válida.", "ERROR");

    let resData: UserData = await res.json();

    return resData;
}
