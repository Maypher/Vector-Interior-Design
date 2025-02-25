export const load = ({ cookies, request }) => {
    const availableLanguages = ["en", "es"];

    let selectedLanguage = cookies.get('lang') || 'en';

    if (!selectedLanguage) {
        const acceptedLanguages = request.headers.get("Accept-Language")?.split(',');
        if (acceptedLanguages) {
            const preferredLang = acceptedLanguages.find((x) => availableLanguages.includes(x.slice(0, 2)))?.slice(0, 2) || 'en';
            selectedLanguage = preferredLang;
        }

        cookies.set('lang', selectedLanguage, { path: '/', httpOnly: false });
    }


    return { selectedLanguage };
}
