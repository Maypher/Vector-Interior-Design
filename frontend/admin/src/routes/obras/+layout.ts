import { type UserData } from "$lib/utilities/interfaces";
import { redirect } from "@sveltejs/kit";
import { PUBLIC_apiUrl } from "$env/static/public";

export async function load({ fetch }) {
    // Determine if user is logged in
    let res = await fetch(PUBLIC_apiUrl + "/auth/info-usuario", {
        credentials: "include"
    });

    if (!res.ok) redirect(302, "/cuenta/");


    let resData: UserData = await res.json();

    return { userData: resData };
}
