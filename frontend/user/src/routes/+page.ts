import { goto } from '$app/navigation'
import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';

export const load = async ({ parent }) => {
    const { selectedLanguage } = await parent();
    const redirectTo = `/${selectedLanguage}`;
    if (browser) await goto(redirectTo);
    else redirect(302, redirectTo);
}
