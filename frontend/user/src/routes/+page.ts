import { goto } from '$app/navigation'
import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';

export const load = async ({ parent }) => {
    const { selectedLanguage } = await parent();
    const redirectTo = `/${selectedLanguage}`;
    redirect(302, redirectTo);
}
