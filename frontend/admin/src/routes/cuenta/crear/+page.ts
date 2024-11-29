import { goto } from '$app/navigation';
import { redirect } from '@sveltejs/kit';
import { browser } from '$app/environment';

export async function load({ parent }) {
    let user_exists = (await parent()).user_exists;

    if (user_exists) {
        if (browser) goto('/cuenta');
        else redirect(302, '/cuenta');
    }
}
