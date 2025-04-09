export const load = ({ locals }): { selectedLanguage: 'en' | 'es' } => {
    return { selectedLanguage: (locals as any).language as 'en' | 'es' };
}
