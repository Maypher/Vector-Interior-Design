import { type UserData } from "$lib/utilities/interfaces";
import { redirect } from "@sveltejs/kit";

export async function load({ fetch }) {
    // Determine if user is logged in
    let res = await fetch("/api/auth/info-usuario");

    if (!res.ok) redirect(302, "/cuenta/");


    let resData: UserData = await res.json();

    return { userData: resData };
}
