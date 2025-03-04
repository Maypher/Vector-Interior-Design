import { setupI18n } from '$lib/i18n';

export const load = async ({ data }) => {
    const i18n = await setupI18n(data.selectedLanguage!);

    return { i18n };
};
