export const load = ({ cookies, request }): { selectedLanguage: 'en' | 'es' } => {
    const availableLanguages = ["en", "es"];

    let selectedLanguage = cookies.get('lang');

    if (!selectedLanguage) {
        const acceptedLanguages = request.headers.get("Accept-Language")?.split(',');
        if (acceptedLanguages) {
            const preferredLang = acceptedLanguages.find((x) => availableLanguages.includes(x.slice(0, 2)))?.slice(0, 2) || 'en';
            selectedLanguage = preferredLang;
        } else selectedLanguage = 'en';
    }


    return { selectedLanguage: selectedLanguage as 'en' | 'es' };
}
